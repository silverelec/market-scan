"""
Competitor Analysis research orchestrator.

Flow:
  1. Claude identifies top 5 competitors
  2. Parallel Tavily + Exa per competitor (5×5 + 5×2 = 35 queries)
  3. 5 parallel Claude calls → 10 sub-sections per competitor
  4. 2 Claude calls → Benchmarking + Cross-competitor, then Exec + Recommendations
"""

import asyncio
import json
import logging
from typing import Any

from anthropic import AsyncAnthropic

from backend.core.config import get_settings
from backend.schemas.request import ScanRequest
from backend.schemas.competitor import (
    CompetitorReport, CompetitorJob, CompetitorProfile,
    Benchmarking, CapabilityBenchmarkRow, FeatureMatrixRow,
    PricingBenchmarkRow, MarketShareRow, SentimentRow,
    PositioningPoint, CrossCompetitorAnalysis, WhiteSpace,
    StrategicRecommendation,
)
from backend.services.researcher import run_research, format_results_as_markdown, get_claude_client

logger = logging.getLogger(__name__)

PER_COMPETITOR_QUERIES = [
    "{competitor} revenue growth financial performance market share",
    "{competitor} products services technology capabilities offerings",
    "{competitor} strategy partnerships acquisitions investments",
    "{competitor} customer segments target markets positioning brand",
    "{competitor} customer reviews reputation sentiment quality",
]

MARKET_CONTEXT_QUERIES = {
    "market_overview": [
        "{market} industry overview size growth demand drivers",
        "{market} value chain structure profit pools",
    ],
    "competitive_context": [
        "{market} competitive landscape key players market share",
    ],
}


async def _identify_competitors(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    company: str,
    market: str,
    additional: list[str],
    date_range: str,
) -> list[str]:
    """Ask Claude to identify top 5 competitors."""
    additional_note = f"\nUser has pre-specified these competitors to include: {', '.join(additional)}" if additional else ""
    prompt = f"""You are a senior management consultant.

Company: {company}
Market: {market}
Date range: {date_range}
{additional_note}

Identify the top 5 companies that most directly compete with {company} in {market}.
Do NOT include {company} itself.
{"Do NOT include: " + ", ".join(additional) + " (already included)" if additional else ""}

Return ONLY valid JSON:
{{
  "competitors": ["Company A", "Company B", "Company C", "Company D", "Company E"]
}}"""
    async with sem:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
        auto = data.get("competitors", [])
    except Exception:
        auto = []

    # Merge auto + user-specified, deduplicated, max 7 total
    all_competitors = []
    seen = {company.lower()}
    for c in (additional + auto):
        if c.lower() not in seen:
            seen.add(c.lower())
            all_competitors.append(c)
        if len(all_competitors) >= 7:
            break
    return all_competitors


async def _research_competitor(
    competitor: str,
    market: str,
    request: ScanRequest,
) -> dict:
    """Run all queries for one competitor, return raw results dict."""
    queries = {
        f"{competitor}_financial": [
            PER_COMPETITOR_QUERIES[0].replace("{competitor}", competitor)
        ],
        f"{competitor}_products": [
            PER_COMPETITOR_QUERIES[1].replace("{competitor}", competitor)
        ],
        f"{competitor}_strategy": [
            PER_COMPETITOR_QUERIES[2].replace("{competitor}", competitor)
        ],
        f"{competitor}_customers": [
            PER_COMPETITOR_QUERIES[3].replace("{competitor}", competitor)
        ],
        f"{competitor}_sentiment": [
            PER_COMPETITOR_QUERIES[4].replace("{competitor}", competitor)
        ],
    }
    exa_q = [
        f"{competitor} analysis report capabilities positioning",
        f"{competitor} {market} strategy competitive advantage",
    ]
    return await run_research(queries, request, exa_queries=exa_q)


async def _synthesize_competitor(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    competitor: str,
    company: str,
    market: str,
    date_range: str,
    raw: dict,
    is_user_specified: bool,
) -> CompetitorProfile:
    """Synthesize all 10 sub-sections for one competitor."""
    context = format_results_as_markdown(
        [r for group in raw.values() for r in group][:30], 8000
    )
    prompt = f"""You are analyzing {competitor} as a competitor to {company} in the {market} market.
Date range: {date_range}

Research data:
{context}

Return ONLY valid JSON with this structure:
{{
  "hq": "City, Country",
  "founded": "Year or approximate",
  "geographic_footprint": ["Region1", "Region2"],
  "revenue_usd_bn": <number or null>,
  "revenue_growth_pct": <number or null>,
  "market_share_pct": <number or null>,
  "employee_count": "approximately X,000",
  "public_private": "Public|Private|PE-backed",
  "revenue_streams": ["stream1", "stream2"],
  "pricing_model": "subscription / per-unit / enterprise",
  "profit_drivers": ["driver1", "driver2"],
  "cost_structure_summary": "brief description",
  "core_offerings": ["offering1", "offering2", "offering3"],
  "differentiators": ["differentiator1", "differentiator2"],
  "technology_capabilities": ["capability1", "capability2"],
  "innovation_pipeline": ["upcoming product/feature"],
  "core_customer_segments": ["segment1", "segment2"],
  "industry_focus": ["industry1", "industry2"],
  "geographic_focus": ["region1", "region2"],
  "key_accounts": ["account1", "account2"],
  "sales_model": "direct / partner / digital / hybrid",
  "distribution_channels": ["channel1", "channel2"],
  "brand_positioning": "1-2 sentence brand narrative",
  "customer_acquisition": "how they acquire customers",
  "recent_acquisitions": ["Company acquired — date — rationale"],
  "product_launches": ["Product launched — date"],
  "strategic_partnerships": ["Partner — purpose"],
  "geographic_expansion": ["Expanded to X"],
  "revenue_trend": "Growing rapidly / Stable / Declining",
  "profitability_trend": "Improving / Stable / Declining",
  "rd_investment": "X% of revenue or $Xbn",
  "financial_strength": "Strong|Moderate|Weak",
  "strengths": ["strength1", "strength2", "strength3", "strength4"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "operational_strengths": ["operational strength1"],
  "customer_sentiment": "Overall positive/negative/mixed with key themes",
  "industry_reputation": "Respected for X, questioned on Y",
  "brand_perception": "How the market perceives them",
  "notable_reviews": ["customer quote or theme"],
  "threat_level": "High|Medium|Low",
  "strongest_competition_areas": ["area1 — why", "area2 — why"],
  "future_risk_potential": "Why this competitor could become more/less dangerous over 3-5 years"
}}

Be factual and specific. Use null for genuinely unknown figures."""

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

    return CompetitorProfile(name=competitor, is_user_specified=is_user_specified, **data)


async def _synthesize_benchmarking(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    company: str,
    competitors: list[CompetitorProfile],
    market: str,
    date_range: str,
) -> tuple[Benchmarking, CrossCompetitorAnalysis]:
    """Sections 4+5: Benchmarking and cross-competitor analysis."""
    all_companies = [company] + [c.name for c in competitors]
    profiles_summary = "\n".join([
        f"- {c.name}: strengths={c.strengths[:2]}, weaknesses={c.weaknesses[:2]}, threat={c.threat_level}"
        for c in competitors
    ])
    prompt = f"""You are comparing {company} against its top competitors in {market}.
Date range: {date_range}

All companies: {', '.join(all_companies)}

Competitor profiles summary:
{profiles_summary}

Return ONLY valid JSON:
{{
  "capability_benchmark": [
    {{
      "company": "Company Name",
      "product_performance": "Leading|Strong|Average|Weak",
      "innovation_technology": "Leading|Strong|Average|Weak",
      "brand_strength": "Leading|Strong|Average|Weak",
      "pricing_competitiveness": "Leading|Strong|Average|Weak",
      "distribution_reach": "Leading|Strong|Average|Weak",
      "partnerships_ecosystem": "Leading|Strong|Average|Weak",
      "customer_experience": "Leading|Strong|Average|Weak"
    }}
  ],
  "feature_matrix": [
    {{
      "feature": "Feature Name",
      "scores": {{"Company1": "Present|Partial|Absent", "Company2": "Present"}}
    }}
  ],
  "pricing_benchmark": [
    {{"company": "Name", "pricing_tier": "Premium|Mid-market|Value", "pricing_model": "subscription", "relative_value": "High|Medium|Low"}}
  ],
  "market_share_comparison": [
    {{"company": "Name", "market_share_pct": <number or null>, "revenue_usd_bn": <number or null>, "yoy_growth_pct": <number or null>}}
  ],
  "sentiment_benchmark": [
    {{"company": "Name", "overall_sentiment": "Positive|Neutral|Negative", "key_themes": ["theme1", "theme2"]}}
  ],
  "positioning_x_axis": "Innovation",
  "positioning_y_axis": "Market Reach",
  "positioning_map": [
    {{"company": "Name", "x_value": <0-10>, "y_value": <0-10>, "is_client": false}}
  ],
  "cross_competitor": {{
    "competitive_battlegrounds": ["battleground1", "battleground2", "battleground3"],
    "client_capability_gaps": ["gap1 — why it matters", "gap2"],
    "client_capability_leads": ["lead1 — advantage", "lead2"],
    "emerging_trends": ["trend1", "trend2", "trend3"],
    "common_strategic_themes": ["theme1 — explanation", "theme2"],
    "industry_investment_direction": "2-3 sentence narrative on where the industry is investing"
  }}
}}

Mark {company} as is_client: true in positioning_map. Include all {len(all_companies)} companies."""

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

    bench = Benchmarking(
        capability_benchmark=[CapabilityBenchmarkRow(**r) for r in data.get("capability_benchmark", [])],
        feature_matrix=[FeatureMatrixRow(**r) for r in data.get("feature_matrix", [])],
        pricing_benchmark=[PricingBenchmarkRow(**r) for r in data.get("pricing_benchmark", [])],
        market_share_comparison=[MarketShareRow(**r) for r in data.get("market_share_comparison", [])],
        sentiment_benchmark=[SentimentRow(**r) for r in data.get("sentiment_benchmark", [])],
        positioning_x_axis=data.get("positioning_x_axis", "Innovation"),
        positioning_y_axis=data.get("positioning_y_axis", "Market Reach"),
        positioning_map=[PositioningPoint(**p) for p in data.get("positioning_map", [])],
    )
    cc_data = data.get("cross_competitor", {})
    cross = CrossCompetitorAnalysis(
        competitive_battlegrounds=cc_data.get("competitive_battlegrounds", []),
        client_capability_gaps=cc_data.get("client_capability_gaps", []),
        client_capability_leads=cc_data.get("client_capability_leads", []),
        emerging_trends=cc_data.get("emerging_trends", []),
        common_strategic_themes=cc_data.get("common_strategic_themes", []),
        industry_investment_direction=cc_data.get("industry_investment_direction", ""),
    )
    return bench, cross


async def _synthesize_strategic(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    company: str,
    competitors: list[CompetitorProfile],
    market: str,
    date_range: str,
    benchmarking: Benchmarking,
    cross: CrossCompetitorAnalysis,
) -> dict:
    """Sections 1+6+7+8: Executive summary, white spaces, implications, recommendations."""
    tops = "\n".join([f"- {c.name}: threat={c.threat_level}, strengths={c.strengths[:2]}" for c in competitors])
    prompt = f"""You are writing the strategic analysis for an MBB-quality competitor analysis report.
Client: {company} — Market: {market} — Date range: {date_range}

Competitive battlegrounds: {cross.competitive_battlegrounds}
Client capability gaps: {cross.client_capability_gaps}
Client capability leads: {cross.client_capability_leads}

Top competitor profiles:
{tops}

Return ONLY valid JSON:
{{
  "purpose": "1-2 sentence purpose of this analysis",
  "key_findings": ["finding1", "finding2", "finding3", "finding4", "finding5"],
  "strategic_implications": ["implication1", "implication2", "implication3"],
  "industry_overview": "2-3 sentence market context",
  "industry_structure_summary": "2-3 sentence value chain and profit pool summary",
  "competitive_landscape_overview": "2-3 sentence competitive dynamics overview",
  "white_spaces": [
    {{"category": "Customer|Product|Geographic|Innovation", "description": "specific white space", "attractiveness": "High|Medium|Low", "rationale": "why it is attractive"}}
  ],
  "competitive_threats": ["specific threat1 to {company}", "threat2", "threat3"],
  "competitive_advantages": ["{company}'s advantage1", "advantage2", "advantage3"],
  "strategic_risks": ["risk1", "risk2", "risk3"],
  "defend": [
    {{"action": "specific action", "rationale": "why", "time_horizon": "Immediate|1-2yr|3-5yr", "expected_impact": "what it achieves"}}
  ],
  "differentiate": [
    {{"action": "specific action", "rationale": "why", "time_horizon": "Immediate|1-2yr|3-5yr", "expected_impact": "what it achieves"}}
  ],
  "expand": [
    {{"action": "specific action", "rationale": "why", "time_horizon": "Immediate|1-2yr|3-5yr", "expected_impact": "what it achieves"}}
  ],
  "strategic_priorities": [
    "Priority 1 — most urgent for {company}",
    "Priority 2",
    "Priority 3",
    "Priority 4",
    "Priority 5"
  ]
}}"""

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
        return json.loads(text)
    except Exception:
        import re
        match = re.search(r'\{[\s\S]*\}', text)
        return json.loads(match.group()) if match else {}


async def build_competitor_analysis(
    request: ScanRequest,
    job: CompetitorJob,
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

        update("identifying", "Identifying top competitors...", 5)
        competitors_list = await _identify_competitors(
            client, sem, company, market, request.additional_competitors, date_range
        )

        update("researching", f"Researching {len(competitors_list)} competitors in parallel...", 15)

        # Research all competitors in parallel
        research_tasks = [
            _research_competitor(c, market, request)
            for c in competitors_list
        ]
        raw_results = await asyncio.gather(*research_tasks, return_exceptions=True)

        update("synthesizing", "Synthesizing competitor profiles...", 40)

        # Synthesize each competitor profile in parallel
        is_user_specified = {c.lower() for c in request.additional_competitors}
        synthesis_tasks = [
            _synthesize_competitor(
                client, sem, competitors_list[i], company, market, date_range,
                raw if not isinstance(raw, Exception) else {},
                competitors_list[i].lower() in is_user_specified,
            )
            for i, raw in enumerate(raw_results)
        ]
        profiles = await asyncio.gather(*synthesis_tasks, return_exceptions=True)
        profiles = [p for p in profiles if isinstance(p, CompetitorProfile)]

        update("synthesizing", "Building benchmarking and strategic analysis...", 70)

        benchmarking, cross = await _synthesize_benchmarking(
            client, sem, company, profiles, market, date_range
        )
        strategic_data = await _synthesize_strategic(
            client, sem, company, profiles, market, date_range, benchmarking, cross
        )

        # Build positioning map for Section 2
        market_pos_map = [
            PositioningPoint(
                company=p.company,
                x_value=p.x_value,
                y_value=p.y_value,
                is_client=p.is_client,
            )
            for p in benchmarking.positioning_map
        ]

        final_report = CompetitorReport(
            company=company, market=market,
            time_period_months=request.time_period_months,
            purpose=strategic_data.get("purpose", ""),
            key_findings=strategic_data.get("key_findings", []),
            strategic_implications=strategic_data.get("strategic_implications", []),
            industry_overview=strategic_data.get("industry_overview", ""),
            industry_structure_summary=strategic_data.get("industry_structure_summary", ""),
            competitive_landscape_overview=strategic_data.get("competitive_landscape_overview", ""),
            positioning_x_axis=benchmarking.positioning_x_axis,
            positioning_y_axis=benchmarking.positioning_y_axis,
            market_positioning_map=market_pos_map,
            competitors=profiles,
            benchmarking=benchmarking,
            cross_competitor=cross,
            white_spaces=[WhiteSpace(**w) for w in strategic_data.get("white_spaces", [])],
            competitive_threats=strategic_data.get("competitive_threats", []),
            competitive_advantages=strategic_data.get("competitive_advantages", []),
            strategic_risks=strategic_data.get("strategic_risks", []),
            defend=[StrategicRecommendation(**r) for r in strategic_data.get("defend", [])],
            differentiate=[StrategicRecommendation(**r) for r in strategic_data.get("differentiate", [])],
            expand=[StrategicRecommendation(**r) for r in strategic_data.get("expand", [])],
            strategic_priorities=strategic_data.get("strategic_priorities", []),
            identified_competitors=competitors_list,
        )

        job.report = final_report
        update("complete", "Competitor analysis complete.", 100)

    except Exception as e:
        logger.exception(f"Competitor analysis failed: {e}")
        job.status = "error"
        job.error = str(e)
        job.progress_message = f"Error: {e}"
        jobs_store[job.job_id] = job
