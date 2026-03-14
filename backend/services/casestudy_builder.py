"""Case Study Generation orchestrator."""

import asyncio
import json
import logging

from anthropic import AsyncAnthropic

from backend.core.config import get_settings
from backend.schemas.request import ScanRequest
from backend.schemas.casestudy import CaseStudyReport, CaseStudyJob, CaseStudy
from backend.services.researcher import run_research, format_results_as_markdown, get_claude_client

logger = logging.getLogger(__name__)

CASE_STUDY_QUERIES = {
    "innovation_tech": ["{market} technology innovation breakthrough 2024 2025"],
    "innovation_model": ["{market} new business model innovation 2024 2025"],
    "innovation_digital": ["{market} digital transformation case study results"],
    "innovation_product": ["{market} product innovation launch success outcomes"],
    "innovation_ops": ["{market} operational innovation efficiency improvement"],
    "innovation_cx": ["{market} customer experience innovation service"],
    "innovation_ai": ["{market} AI automation machine learning implementation results"],
    "innovation_disruption": ["{market} startup disruption new entrant innovation"],
    "innovation_esg": ["{market} ESG sustainability innovation green initiative"],
    "innovation_platform": ["{market} platform ecosystem partnership innovation"],
    "company_context": [
        "{company} innovation strategy {market}",
        "{company} {market} technology investment",
    ],
}

EXA_QUERIES = [
    "{market} innovation case study success story analysis",
    "{market} breakthrough technology implementation report",
    "{market} business model innovation whitepaper",
    "{company} innovation opportunity {market}",
    "{market} future trends disruption analysis",
]


async def _identify_innovations(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    company: str,
    market: str,
    date_range: str,
    raw: dict,
) -> list[dict]:
    """Identify the top 5 distinct innovations from search results."""
    context = format_results_as_markdown(
        [r for group in raw.values() for r in group][:40], 10000
    )
    prompt = f"""You are a senior management consultant identifying the most impactful innovations in the {market} market for a report targeting {company}.
Date range: {date_range}

Research findings:
{context}

Identify the top 5 DISTINCT innovations — ensure they cover different categories: Technology, Business Model, Operations, Customer Experience, and ESG/Sustainability.

Return ONLY valid JSON:
{{
  "innovations": [
    {{
      "title": "Concise innovation title (5-8 words)",
      "innovation_type": "Technology|Business Model|Operations|Customer|ESG",
      "lead_company": "Primary company exemplifying this innovation",
      "brief_description": "1-2 sentence description of the innovation"
    }}
  ]
}}

Each innovation must be distinct and concrete. No duplicates."""

    async with sem:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
        return data.get("innovations", [])
    except Exception:
        return []


async def _build_case_study(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    number: int,
    innovation: dict,
    company: str,
    market: str,
    date_range: str,
    raw: dict,
) -> CaseStudy:
    """Build full 5-section case study for one innovation."""
    # Get relevant context from search results
    lead = innovation.get("lead_company", "")
    title = innovation.get("title", "")
    itype = innovation.get("innovation_type", "")

    relevant = []
    for group_results in raw.values():
        for r in group_results:
            if any(kw.lower() in r.content.lower() or kw.lower() in r.title.lower()
                   for kw in [lead, title, itype.lower(), market.lower()]):
                relevant.append(r)
    context = format_results_as_markdown((relevant or list(raw.values())[0])[:15], 5000)

    prompt = f"""You are writing Case Study #{number} for an MBB-quality innovation report.

Innovation: {title}
Type: {itype}
Lead Company: {lead}
Client: {company}
Market: {market}
Date Range: {date_range}

Research context:
{context}

Write a detailed, factual case study. Return ONLY valid JSON:
{{
  "title": "{title}",
  "innovation_description": "1-2 sentence precise description of what the innovation is",
  "problem_solved": "What specific problem or unmet need this addresses",
  "where_emerging": "Where in the {market} industry this is emerging and gaining traction",
  "lead_company": "{lead}",
  "implementation_description": "How {lead} (or the leading example) implemented this — be specific about approach, timeline, scale",
  "metrics_outcomes": [
    "Specific metric or outcome (e.g., 30% cost reduction, 2x revenue growth)",
    "Another measurable outcome",
    "A third outcome"
  ],
  "customer_impact": "How customers experience this innovation — value delivered, experience changes",
  "business_performance_impact": "Revenue, cost, efficiency, or margin impact on businesses that adopt this",
  "competitive_dynamics_impact": "How this shifts the competitive landscape — who wins, who loses, what changes",
  "key_takeaways": [
    "Why this innovation works — the core mechanism of success",
    "What makes it successful — critical success factors",
    "What others in {market} can learn and apply",
    "A fourth takeaway if applicable"
  ],
  "client_relevance": "Specific explanation of why this matters to {company} given their position in {market}",
  "potential_opportunity": "Concrete opportunity or implication for {company} — what they could do with this",
  "innovation_type": "{itype}",
  "maturity_level": "Emerging|Scaling|Mainstream"
}}

Be specific and factual. Each bullet and sentence must add insight, not filler."""

    async with sem:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=get_settings().claude_max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
    except Exception:
        import re
        match = re.search(r'\{[\s\S]*\}', text)
        data = json.loads(match.group()) if match else {}

    return CaseStudy(number=number, **data)


async def build_case_studies(
    request: ScanRequest,
    job: CaseStudyJob,
    jobs_store: dict,
) -> None:
    def update(status, msg, pct):
        job.status = status
        job.progress_message = msg
        job.progress_pct = pct
        jobs_store[job.job_id] = job

    try:
        settings = get_settings()
        client = get_claude_client()
        sem = asyncio.Semaphore(settings.concurrent_claude_calls)
        company = request.company
        market = request.market
        date_range = request.date_range_label

        update("researching", "Searching for innovations across the market...", 10)

        queries = {
            k: [q.replace("{company}", company).replace("{market}", market) for q in v]
            for k, v in CASE_STUDY_QUERIES.items()
        }
        exa_q = [q.replace("{company}", company).replace("{market}", market) for q in EXA_QUERIES]
        raw = await run_research(queries, request, exa_queries=exa_q)

        update("identifying", "Identifying top 5 innovations...", 35)
        innovations = await _identify_innovations(client, sem, company, market, date_range, raw)

        if not innovations:
            raise ValueError("Could not identify innovations from search results")

        update("synthesizing", "Building 5 case studies in parallel...", 50)

        tasks = [
            _build_case_study(client, sem, i + 1, inv, company, market, date_range, raw)
            for i, inv in enumerate(innovations[:5])
        ]
        case_studies = await asyncio.gather(*tasks, return_exceptions=True)
        case_studies = [cs for cs in case_studies if isinstance(cs, CaseStudy)]

        # Collect sources
        all_sources = []
        seen_urls: set[str] = set()
        for group in raw.values():
            for r in group:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    all_sources.append({"url": r.url, "title": r.title, "published_date": r.published_date, "source": r.source})

        final_report = CaseStudyReport(
            company=company, market=market,
            time_period_months=request.time_period_months,
            case_studies=case_studies,
            report_narrative=f"Five innovation case studies from the {market} market, curated for {company}. Each case study is drawn from real-world examples within the analysis period ({date_range}) and includes explicit strategic implications for {company}.",
            all_sources=all_sources[:40],
        )

        job.report = final_report
        update("complete", "Case studies complete.", 100)

    except Exception as e:
        logger.exception(f"Case study generation failed: {e}")
        job.status = "error"
        job.error = str(e)
        job.progress_message = f"Error: {e}"
        jobs_store[job.job_id] = job
