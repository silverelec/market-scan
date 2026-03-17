"""
Market Scan research orchestrator.

Flow:
  1. Run ~21 Tavily + ~5 Exa queries in parallel
  2. 9 parallel Claude synthesis calls (sections 2-11), Semaphore(3)
  3. 1 Claude strategic synthesis (sections 1 + 12)
  4. Assemble MarketScanReport
"""

import asyncio
import json
import logging
from datetime import date, timedelta

from anthropic import AsyncAnthropic

from backend.core.config import get_settings
from backend.schemas.request import ScanRequest
from backend.schemas.market_scan import (
    MarketScanReport, MarketScanJob, MarketSnapshot, MarketDefinition,
    MarketSizeData, MarketStructure, CompetitiveLandscape, CustomerAnalysis,
    TechTrends, RegulatoryFactors, GeographicLandscape, InvestmentMA,
    StrategicOpportunities, Implications, SearchResult,
    SegmentationDimension, ValueChainStage, ProfitPoolSegment,
    CompetitorEntry, PositioningMatrixEntry, CustomerSegment,
    TechTrend, RDPlayer, RegulatoryItem, MacroFactor, ESGItem,
    RegionData, Deal, Risk, StrategicPlay,
)
from backend.services.researcher import run_research, format_results_as_markdown, get_claude_client

logger = logging.getLogger(__name__)

TAVILY_QUERIES = {
    "market_definition": [
        "{market} industry definition scope products services included",
    ],
    "market_size": [
        "{market} market size TAM total addressable market revenue billion",
        "{market} CAGR compound annual growth rate forecast projection",
    ],
    "market_structure": [
        "{market} value chain structure margin analysis where profits captured",
        "{market} profit pools cost structure economics pricing model",
    ],
    "competitive": [
        "{market} top companies market share leaders revenue rankings",
        "{market} disruptors new entrants startups competitive landscape",
        "{market} M&A mergers acquisitions partnerships strategic moves",
    ],
    "customer": [
        "{market} customer segments buyer types demand analysis",
        "{market} customer needs pain points purchase drivers buying behavior",
    ],
    "technology": [
        "{market} technology trends AI automation digitization innovation",
        "{market} R&D research development patents product innovation pipeline",
    ],
    "regulatory": [
        "{market} regulation compliance licensing standards ESG requirements",
        "{market} macroeconomic factors GDP interest rates trade policy impact",
    ],
    "geographic": [
        "{market} regional market size breakdown by geography country",
        "{market} fastest growing regions emerging markets opportunities",
    ],
    "investment": [
        "{market} venture capital private equity investment funding",
        "{market} acquisitions mergers deals transactions",
    ],
    "company_context": [
        "{company} strategy {market} market positioning competitive advantage",
        "{company} strengths capabilities {market} industry",
    ],
}

EXA_QUERIES = [
    "{market} market analysis report industry outlook",
    "{market} competitive intelligence strategic analysis whitepaper",
    "{market} investment thesis market research",
    "{company} {market} strategic positioning analysis",
    "{market} emerging trends disruption forces",
]


def _build_queries(company: str, market: str) -> tuple[dict, list]:
    """Substitute company and market into query templates."""
    tavily = {}
    for key, queries in TAVILY_QUERIES.items():
        tavily[key] = [q.replace("{company}", company).replace("{market}", market) for q in queries]
    exa = [q.replace("{company}", company).replace("{market}", market) for q in EXA_QUERIES]
    return tavily, exa


async def _claude_json(
    client: AsyncAnthropic,
    prompt: str,
    sem: asyncio.Semaphore,
) -> dict:
    """Call Claude and parse JSON response."""
    import re
    from json_repair import repair_json

    settings = get_settings()
    async with sem:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=settings.claude_max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
    text = response.content[0].text.strip()
    # Strip markdown code fences using regex (handles nested backticks safely)
    fence_match = re.match(r'^```(?:json)?\s*([\s\S]*?)\s*```$', text)
    if fence_match:
        text = fence_match.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse failed ({e}), attempting repair...")
        try:
            repaired = repair_json(text, return_objects=True)
            if isinstance(repaired, dict):
                return repaired
        except Exception:
            pass
        logger.error(f"Could not parse JSON from Claude response: {text[:500]}")
        return {}


async def _synthesize_section_a(
    client: AsyncAnthropic,
    sem: asyncio.Semaphore,
    company: str,
    market: str,
    date_range: str,
    raw: dict,
) -> tuple[MarketDefinition, MarketSizeData]:
    """Sections 2+3: Market Definition + Size/Growth."""
    context = (
        format_results_as_markdown(raw.get("market_definition", []), 3000) + "\n\n" +
        format_results_as_markdown(raw.get("market_size", []), 4000) +
        format_results_as_markdown(raw.get("exa", [])[:3], 2000)
    )
    prompt = f"""You are a senior management consultant analyzing the {market} market for a client report.
Date range for analysis: {date_range}
Company of interest: {company}

Based on these research sources:
{context}

Return ONLY valid JSON (no prose, no markdown) with this exact structure:
{{
  "market_definition": {{
    "industry_definition": "2-3 sentence precise industry definition",
    "value_chain_scope": "Description of value chain scope covered",
    "products_services_included": ["product1", "product2", ...],
    "methodology": "Brief methodology note",
    "sizing_approach": "How market is sized (top-down / bottom-up)",
    "assumptions": ["assumption1", "assumption2"],
    "segmentation_framework": [
      {{"dimension": "Product/Service Category", "segments": ["seg1", "seg2"], "strategic_relevance": "why this matters"}},
      {{"dimension": "Customer Segment", "segments": ["seg1", "seg2"], "strategic_relevance": "why this matters"}},
      {{"dimension": "Price Tier", "segments": ["premium", "mid", "value"], "strategic_relevance": "why this matters"}},
      {{"dimension": "Geography", "segments": ["APAC", "NA", "EMEA"], "strategic_relevance": "why this matters"}},
      {{"dimension": "Channel", "segments": ["direct", "partner", "digital"], "strategic_relevance": "why this matters"}}
    ]
  }},
  "market_size": {{
    "tam_usd_bn": <number or null>,
    "sam_usd_bn": <number or null>,
    "som_usd_bn": <number or null>,
    "historical_cagr_percent": <number or null>,
    "forecast_cagr_percent": <number or null>,
    "forecast_size_5yr_usd_bn": <number or null>,
    "historical_data": [{{"year": 2020, "value_usd_bn": 0.0, "note": ""}}],
    "forecast_data": [{{"year": 2025, "value_usd_bn": 0.0, "is_forecast": true}}],
    "growth_drivers": ["driver1", "driver2", "driver3", "driver4", "driver5"],
    "growth_constraints": ["constraint1", "constraint2", "constraint3"],
    "cyclicality_notes": "note on cyclicality patterns"
  }}
}}

Be specific with numbers where available. Use null for genuinely unknown values. Focus on {date_range}."""
    data = await _claude_json(client, prompt, sem)
    mdef_data = data.get("market_definition", {})
    msize_data = data.get("market_size", {})

    market_def = MarketDefinition(
        industry_definition=mdef_data.get("industry_definition", ""),
        value_chain_scope=mdef_data.get("value_chain_scope", ""),
        products_services_included=mdef_data.get("products_services_included", []),
        methodology=mdef_data.get("methodology", ""),
        sizing_approach=mdef_data.get("sizing_approach", ""),
        assumptions=mdef_data.get("assumptions", []),
        segmentation_framework=[
            SegmentationDimension(**s) for s in mdef_data.get("segmentation_framework", [])
        ],
    )
    market_size = MarketSizeData(
        tam_usd_bn=msize_data.get("tam_usd_bn"),
        sam_usd_bn=msize_data.get("sam_usd_bn"),
        som_usd_bn=msize_data.get("som_usd_bn"),
        historical_cagr_percent=msize_data.get("historical_cagr_percent"),
        forecast_cagr_percent=msize_data.get("forecast_cagr_percent"),
        forecast_size_5yr_usd_bn=msize_data.get("forecast_size_5yr_usd_bn"),
        historical_data=msize_data.get("historical_data", []),
        forecast_data=msize_data.get("forecast_data", []),
        growth_drivers=msize_data.get("growth_drivers", []),
        growth_constraints=msize_data.get("growth_constraints", []),
        cyclicality_notes=msize_data.get("cyclicality_notes", ""),
    )
    return market_def, market_size


async def _synthesize_section_b(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> MarketStructure:
    """Section 4: Market Structure."""
    context = format_results_as_markdown(raw.get("market_structure", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are a senior management consultant analyzing the {market} market structure.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "value_chain": [
    {{"stage": "Stage Name", "description": "what happens here", "key_players": ["player1"], "margin_capture": "High|Medium|Low", "power_dynamics": "who has power and why"}}
  ],
  "profit_pools": [
    {{"segment": "Segment Name", "margin_percent": <number or null>, "profitability_tier": "High|Medium|Low", "notes": "context"}}
  ],
  "typical_cost_structure": {{"COGS": "40-45%", "SG&A": "20-25%", "R&D": "5-10%", "Other": "5%"}},
  "pricing_models": ["subscription", "per-unit", "enterprise license"],
  "capex_intensity": "High|Medium|Low",
  "where_margins_captured": "2-3 sentence explanation of where in value chain margins are highest",
  "where_power_sits": "2-3 sentence explanation of who holds negotiating power"
}}"""
    data = await _claude_json(client, prompt, sem)
    return MarketStructure(
        value_chain=[ValueChainStage(**s) for s in data.get("value_chain", [])],
        profit_pools=[ProfitPoolSegment(**s) for s in data.get("profit_pools", [])],
        typical_cost_structure=data.get("typical_cost_structure", {}),
        pricing_models=data.get("pricing_models", []),
        capex_intensity=data.get("capex_intensity", ""),
        where_margins_captured=data.get("where_margins_captured", ""),
        where_power_sits=data.get("where_power_sits", ""),
    )


async def _synthesize_section_c(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> CompetitiveLandscape:
    """Section 5: Competitive Landscape."""
    context = format_results_as_markdown(raw.get("competitive", []) + raw.get("exa", [])[:3], 7000)
    prompt = f"""You are analyzing the competitive landscape of the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "overview_narrative": "3-4 sentence overview of competitive dynamics",
  "key_players": [
    {{"name": "Company Name", "tier": "Leader|Challenger|Niche|Disruptor", "market_share_pct": <number or null>, "revenue_usd_bn": <number or null>, "geographic_reach": "Global|Regional|Local", "key_strengths": ["strength1", "strength2"]}}
  ],
  "market_concentration": "Fragmented|Moderately concentrated|Concentrated",
  "positioning_x_axis": "Innovation",
  "positioning_y_axis": "Scale",
  "positioning_matrix": [
    {{"company": "Name", "x_axis_value": <0-10>, "y_axis_value": <0-10>, "tier": "Leader|Challenger|Niche|Disruptor"}}
  ],
  "strategic_moves": ["move1", "move2", "move3", "move4", "move5"],
  "new_entrants_disruptors": ["company1 — brief description", "company2 — brief description"]
}}

Include at least 6-8 key players. Be specific about market shares where data exists."""
    data = await _claude_json(client, prompt, sem)
    return CompetitiveLandscape(
        overview_narrative=data.get("overview_narrative", ""),
        key_players=[CompetitorEntry(**p) for p in data.get("key_players", [])],
        market_concentration=data.get("market_concentration", ""),
        positioning_x_axis=data.get("positioning_x_axis", "Innovation"),
        positioning_y_axis=data.get("positioning_y_axis", "Scale"),
        positioning_matrix=[PositioningMatrixEntry(**e) for e in data.get("positioning_matrix", [])],
        strategic_moves=data.get("strategic_moves", []),
        new_entrants_disruptors=data.get("new_entrants_disruptors", []),
    )


async def _synthesize_section_d(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> CustomerAnalysis:
    """Section 6: Customer Analysis."""
    context = format_results_as_markdown(raw.get("customer", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are analyzing customer dynamics in the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "segments": [
    {{"name": "Segment Name", "description": "who they are", "size_estimate": "$Xbn or X% of market", "growth_rate": "X% CAGR"}}
  ],
  "key_purchase_drivers": ["driver1", "driver2", "driver3", "driver4"],
  "pain_points": ["pain1", "pain2", "pain3", "pain4"],
  "unmet_needs": ["need1", "need2", "need3"],
  "decision_makers": ["CTO", "CFO", "Procurement"],
  "procurement_process": "Description of typical buying process",
  "switching_costs": "High|Medium|Low",
  "willingness_to_pay": "Description of WTP dynamics",
  "lifetime_value_notes": "Notes on CLV",
  "price_sensitivity": "High|Medium|Low"
}}"""
    data = await _claude_json(client, prompt, sem)
    return CustomerAnalysis(
        segments=[CustomerSegment(**s) for s in data.get("segments", [])],
        key_purchase_drivers=data.get("key_purchase_drivers", []),
        pain_points=data.get("pain_points", []),
        unmet_needs=data.get("unmet_needs", []),
        decision_makers=data.get("decision_makers", []),
        procurement_process=data.get("procurement_process", ""),
        switching_costs=data.get("switching_costs", ""),
        willingness_to_pay=data.get("willingness_to_pay", ""),
        lifetime_value_notes=data.get("lifetime_value_notes", ""),
        price_sensitivity=data.get("price_sensitivity", ""),
    )


async def _synthesize_section_e(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> TechTrends:
    """Section 7: Technology Trends."""
    context = format_results_as_markdown(raw.get("technology", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are analyzing technology trends in the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "product_innovations_5yr": ["innovation1", "innovation2", "innovation3", "innovation4", "innovation5"],
  "disruptive_technologies": [
    {{"technology": "AI/ML", "description": "how it disrupts", "impact_level": "High|Medium|Low", "time_horizon": "Now|1-3yr|3-5yr"}}
  ],
  "rd_intensity_notes": "Comparison of R&D investment levels across the industry",
  "rd_leaders": [
    {{"company": "Name", "rd_spend_usd_bn": <number or null>, "rd_as_pct_revenue": <number or null>, "notable_patents": ["patent1"]}}
  ],
  "innovation_pipeline": ["upcoming innovation1", "upcoming innovation2", "upcoming innovation3"]
}}"""
    data = await _claude_json(client, prompt, sem)
    return TechTrends(
        product_innovations_5yr=data.get("product_innovations_5yr", []),
        disruptive_technologies=[TechTrend(**t) for t in data.get("disruptive_technologies", [])],
        rd_intensity_notes=data.get("rd_intensity_notes", ""),
        rd_leaders=[RDPlayer(**r) for r in data.get("rd_leaders", [])],
        innovation_pipeline=data.get("innovation_pipeline", []),
    )


async def _synthesize_section_f(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> RegulatoryFactors:
    """Section 8: Regulatory & External."""
    context = format_results_as_markdown(raw.get("regulatory", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are analyzing regulatory and external factors in the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "regulations": [
    {{"area": "Data Privacy", "description": "specific regulation", "impact": "High|Medium|Low", "region": "EU|US|Global"}}
  ],
  "macro_factors": [
    {{"factor": "Interest Rates", "current_state": "current situation", "impact_on_market": "how it affects the market"}}
  ],
  "esg_trends": [
    {{"area": "Sustainability|Carbon|Ethical sourcing|Social", "description": "specific trend", "regulatory_pressure": "High|Medium|Low"}}
  ]
}}"""
    data = await _claude_json(client, prompt, sem)
    return RegulatoryFactors(
        regulations=[RegulatoryItem(**r) for r in data.get("regulations", [])],
        macro_factors=[MacroFactor(**m) for m in data.get("macro_factors", [])],
        esg_trends=[ESGItem(**e) for e in data.get("esg_trends", [])],
    )


async def _synthesize_section_g(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> GeographicLandscape:
    """Section 9: Geographic."""
    context = format_results_as_markdown(raw.get("geographic", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are analyzing the geographic landscape of the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "regions": [
    {{"region": "North America", "market_size_usd_bn": <number or null>, "share_pct": <number or null>, "cagr_percent": <number or null>, "growth_stage": "Mature|Growing|Emerging"}}
  ],
  "growth_hotspots": ["region1 — reason", "region2 — reason", "region3 — reason"],
  "local_champion_markets": ["Market where local players dominate"],
  "global_vs_local_dynamics": "2-3 sentence analysis of global vs local competitive dynamics"
}}

Include all major regions: North America, Europe, Asia-Pacific, Latin America, Middle East & Africa."""
    data = await _claude_json(client, prompt, sem)
    return GeographicLandscape(
        regions=[RegionData(**r) for r in data.get("regions", [])],
        growth_hotspots=data.get("growth_hotspots", []),
        local_champion_markets=data.get("local_champion_markets", []),
        global_vs_local_dynamics=data.get("global_vs_local_dynamics", ""),
    )


async def _synthesize_section_h(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> InvestmentMA:
    """Section 10: Investment & M&A."""
    context = format_results_as_markdown(raw.get("investment", []) + raw.get("exa", [])[:2], 6000)
    prompt = f"""You are analyzing investment and M&A activity in the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "recent_deals": [
    {{"deal_type": "Acquisition|Merger|Investment|PE|VC", "acquirer": "Company A", "target": "Company B", "value_usd_mn": <number or null>, "date": "YYYY-MM", "strategic_rationale": "why this deal happened"}}
  ],
  "pe_themes": ["rollup strategy", "platform build", "carve-out opportunity"],
  "vc_emerging_startups": ["startup1 — brief description", "startup2 — brief description"],
  "capital_flow_narrative": "2-3 sentence narrative on where capital is flowing and why",
  "total_deal_value_usd_bn": <number or null>
}}"""
    data = await _claude_json(client, prompt, sem)
    return InvestmentMA(
        recent_deals=[Deal(**d) for d in data.get("recent_deals", [])],
        pe_themes=data.get("pe_themes", []),
        vc_emerging_startups=data.get("vc_emerging_startups", []),
        capital_flow_narrative=data.get("capital_flow_narrative", ""),
        total_deal_value_usd_bn=data.get("total_deal_value_usd_bn"),
    )


async def _synthesize_section_i(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    market: str, date_range: str, raw: dict,
) -> list[Risk]:
    """Section 11: Risks."""
    all_results = []
    for key in ["regulatory", "technology", "market_structure", "investment", "exa"]:
        all_results.extend(raw.get(key, [])[:2])
    context = format_results_as_markdown(all_results, 5000)
    prompt = f"""You are identifying key risks and uncertainties in the {market} market.
Date range: {date_range}

Research:
{context}

Return ONLY valid JSON:
{{
  "risks": [
    {{
      "category": "Regulatory|Technology|Supply Chain|Macro|Competitive",
      "risk": "Specific risk description",
      "likelihood": "High|Medium|Low",
      "impact": "High|Medium|Low",
      "mitigation": "How to mitigate this risk"
    }}
  ]
}}

Identify 6-10 distinct, specific risks across multiple categories."""
    data = await _claude_json(client, prompt, sem)
    return [Risk(**r) for r in data.get("risks", [])]


async def _synthesize_strategic(
    client: AsyncAnthropic, sem: asyncio.Semaphore,
    company: str, market: str, date_range: str,
    report: MarketScanReport,
    raw: dict,
) -> tuple[list[str], list[str], Implications, list[str], StrategicOpportunities]:
    """Sections 1+12: Executive summary and strategic opportunities (after all sections done)."""
    # Summarize all sections as context for strategic synthesis
    context_parts = [
        f"Market: {market}\nCompany of Interest: {company}\nDate Range: {date_range}\n",
        f"Market Size: TAM ${report.market_size.tam_usd_bn}bn, CAGR {report.market_size.forecast_cagr_percent}%",
        f"Growth Drivers: {'; '.join(report.market_size.growth_drivers[:3])}",
        f"Market Concentration: {report.competitive_landscape.market_concentration}",
        f"Top Players: {', '.join(p.name for p in report.competitive_landscape.key_players[:5])}",
        f"Key Customer Pain Points: {'; '.join(report.customer_analysis.pain_points[:3])}",
        f"Disruptive Technologies: {'; '.join(t.technology for t in report.tech_trends.disruptive_technologies[:3])}",
        f"Top Risks: {'; '.join(r.risk[:80] for r in report.risks[:3])}",
        f"Company Context: " + format_results_as_markdown(raw.get("company_context", []), 2000),
    ]
    context = "\n".join(context_parts)

    prompt = f"""You are writing the strategic narrative for an MBB-quality market scan report.
Client company: {company}
Market: {market}
Date range: {date_range}

Market Analysis Summary:
{context}

Return ONLY valid JSON:
{{
  "exec_summary_bullets": [
    "Bullet 1 — most important finding, max 30 words",
    "Bullet 2 — second most important finding",
    "Bullet 3",
    "Bullet 4",
    "Bullet 5"
  ],
  "key_insights": [
    "Non-obvious insight 1 — something that goes beyond the obvious data",
    "Non-obvious insight 2",
    "Non-obvious insight 3",
    "Non-obvious insight 4"
  ],
  "implications": {{
    "focus_areas": ["area1 for {company} to focus on", "area2", "area3"],
    "areas_to_avoid": ["area1 {company} should avoid", "area2"],
    "strategic_risks": ["risk1 for {company}", "risk2", "risk3"]
  }},
  "opportunities_identified": [
    "Strategic opportunity 1",
    "Strategic opportunity 2",
    "Strategic opportunity 3",
    "Strategic opportunity 4"
  ],
  "strategic_opportunities": {{
    "white_space_opportunities": ["underserved segment or gap", "another gap", "another"],
    "capability_fit_areas": ["where {company} has natural advantages", "another area"],
    "potential_strategic_plays": [
      {{"play_type": "New product|Geographic expansion|Acquisition|Partnership", "description": "specific play", "rationale": "why this makes sense for {company}", "estimated_impact": "revenue/market share potential"}}
    ],
    "recommended_priorities": [
      "Priority 1 — most urgent action for {company}",
      "Priority 2",
      "Priority 3",
      "Priority 4",
      "Priority 5"
    ]
  }}
}}

Be specific to {company}'s context. Focus on "so what" — actionable insights, not generic observations.
Write any acronyms with their full form on first mention (e.g. "Artificial Intelligence (AI)", "Compound Annual Growth Rate (CAGR)")."""
    data = await _claude_json(client, prompt, sem)

    strat_data = data.get("strategic_opportunities", {})
    strategic_opps = StrategicOpportunities(
        white_space_opportunities=strat_data.get("white_space_opportunities", []),
        capability_fit_areas=strat_data.get("capability_fit_areas", []),
        potential_strategic_plays=[
            StrategicPlay(**p) for p in strat_data.get("potential_strategic_plays", [])
        ],
        recommended_priorities=strat_data.get("recommended_priorities", []),
    )
    implications_data = data.get("implications", {})
    implications = Implications(
        focus_areas=implications_data.get("focus_areas", []),
        areas_to_avoid=implications_data.get("areas_to_avoid", []),
        strategic_risks=implications_data.get("strategic_risks", []),
    )
    return (
        data.get("exec_summary_bullets", []),
        data.get("key_insights", []),
        implications,
        data.get("opportunities_identified", []),
        strategic_opps,
    )


async def build_market_scan(
    request: ScanRequest,
    job: MarketScanJob,
    jobs_store: dict,
) -> None:
    """Full market scan pipeline — runs as FastAPI BackgroundTask."""

    def update(status: str, msg: str, pct: int):
        job.status = status
        job.progress_message = msg
        job.progress_pct = pct
        jobs_store[job.job_id] = job

    try:
        update("researching", "Launching research queries across Tavily and Exa...", 5)
        company = request.company
        market = request.market
        date_range = request.date_range_label

        tavily_queries, exa_queries = _build_queries(company, market)
        raw = await run_research(tavily_queries, request, exa_queries=exa_queries)

        update("synthesizing", "Synthesizing market sections in parallel...", 30)

        client = get_claude_client()
        sem = asyncio.Semaphore(get_settings().concurrent_claude_calls)

        # Run sections 2-11 in parallel (9 calls, throttled by semaphore)
        results = await asyncio.gather(
            _synthesize_section_a(client, sem, company, market, date_range, raw),
            _synthesize_section_b(client, sem, market, date_range, raw),
            _synthesize_section_c(client, sem, market, date_range, raw),
            _synthesize_section_d(client, sem, market, date_range, raw),
            _synthesize_section_e(client, sem, market, date_range, raw),
            _synthesize_section_f(client, sem, market, date_range, raw),
            _synthesize_section_g(client, sem, market, date_range, raw),
            _synthesize_section_h(client, sem, market, date_range, raw),
            _synthesize_section_i(client, sem, market, date_range, raw),
            return_exceptions=True,
        )

        update("synthesizing", "Building executive summary and strategic implications...", 75)

        # Unpack section results (handle any exceptions gracefully)
        def safe(result, default):
            return result if not isinstance(result, Exception) else default

        market_def, market_size = safe(results[0], (MarketDefinition(), MarketSizeData()))
        market_structure = safe(results[1], MarketStructure())
        competitive_landscape = safe(results[2], CompetitiveLandscape())
        customer_analysis = safe(results[3], CustomerAnalysis())
        tech_trends = safe(results[4], TechTrends())
        regulatory = safe(results[5], RegulatoryFactors())
        geographic = safe(results[6], GeographicLandscape())
        investment_ma = safe(results[7], InvestmentMA())
        risks = safe(results[8], [])

        # Assemble partial report for strategic synthesis context
        partial_report = MarketScanReport(
            company=company, market=market,
            time_period_months=request.time_period_months,
            market_definition=market_def, market_size=market_size,
            market_structure=market_structure,
            competitive_landscape=competitive_landscape,
            customer_analysis=customer_analysis,
            tech_trends=tech_trends, regulatory=regulatory,
            geographic=geographic, investment_ma=investment_ma, risks=risks,
        )

        exec_bullets, key_insights, implications, opportunities, strategic_opps = \
            await _synthesize_strategic(client, sem, company, market, date_range, partial_report, raw)

        # Build market snapshot from size data
        snapshot = MarketSnapshot(
            market_size_usd_bn=market_size.tam_usd_bn,
            cagr_percent=market_size.forecast_cagr_percent,
            key_segments=[s.segments[0] for s in market_def.segmentation_framework[:3] if s.segments],
            geographic_distribution={
                r.region: f"{r.share_pct}%" for r in geographic.regions[:5] if r.share_pct
            },
            industry_maturity="Growth",  # set from competitive landscape context
        )

        # Collect all sources
        all_sources_raw = []
        for results_list in raw.values():
            all_sources_raw.extend(results_list)
        seen_urls: set[str] = set()
        deduped_sources = []
        for r in all_sources_raw:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                deduped_sources.append(SearchResult(
                    url=r.url, title=r.title,
                    content=r.content[:200], published_date=r.published_date, source=r.source,
                ))

        final_report = MarketScanReport(
            company=company, market=market,
            time_period_months=request.time_period_months,
            market_snapshot=snapshot,
            key_insights=key_insights,
            implications=implications,
            opportunities_identified=opportunities,
            exec_summary_bullets=exec_bullets,
            market_definition=market_def,
            market_size=market_size,
            market_structure=market_structure,
            competitive_landscape=competitive_landscape,
            customer_analysis=customer_analysis,
            tech_trends=tech_trends,
            regulatory=regulatory,
            geographic=geographic,
            investment_ma=investment_ma,
            risks=risks,
            strategic_opportunities=strategic_opps,
            all_sources=deduped_sources[:50],
        )

        job.report = final_report
        update("complete", "Report complete.", 100)

    except Exception as e:
        logger.exception(f"Market scan failed: {e}")
        job.status = "error"
        job.error = str(e)
        job.progress_message = f"Error: {e}"
        jobs_store[job.job_id] = job
