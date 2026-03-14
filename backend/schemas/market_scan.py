from pydantic import BaseModel, Field
from typing import Literal, Any
import uuid
from datetime import datetime


class SearchResult(BaseModel):
    url: str
    title: str
    content: str
    published_date: str
    source: str  # "tavily" | "exa"


# ── Section 1: Executive Summary ─────────────────────────────────────────────

class MarketSnapshot(BaseModel):
    market_size_usd_bn: float | None = None
    cagr_percent: float | None = None
    key_segments: list[str] = []
    geographic_distribution: dict[str, str] = {}  # region → % share
    industry_maturity: str = ""  # Emerging | Growth | Mature | Declining

class Implications(BaseModel):
    focus_areas: list[str] = []
    areas_to_avoid: list[str] = []
    strategic_risks: list[str] = []

# ── Section 2: Market Definition ─────────────────────────────────────────────

class SegmentationDimension(BaseModel):
    dimension: str  # Product, Customer, Price Tier, Geography, Channel
    segments: list[str]
    strategic_relevance: str

class MarketDefinition(BaseModel):
    industry_definition: str = ""
    value_chain_scope: str = ""
    products_services_included: list[str] = []
    methodology: str = ""
    sizing_approach: str = ""
    assumptions: list[str] = []
    segmentation_framework: list[SegmentationDimension] = []

# ── Section 3: Market Size & Growth ──────────────────────────────────────────

class HistoricalDataPoint(BaseModel):
    year: int
    value_usd_bn: float
    note: str = ""

class ForecastDataPoint(BaseModel):
    year: int
    value_usd_bn: float
    is_forecast: bool = True

class MarketSizeData(BaseModel):
    tam_usd_bn: float | None = None
    sam_usd_bn: float | None = None
    som_usd_bn: float | None = None
    historical_cagr_percent: float | None = None
    forecast_cagr_percent: float | None = None
    forecast_size_5yr_usd_bn: float | None = None
    historical_data: list[HistoricalDataPoint] = []
    forecast_data: list[ForecastDataPoint] = []
    growth_drivers: list[str] = []
    growth_constraints: list[str] = []
    cyclicality_notes: str = ""

# ── Section 4: Market Structure ───────────────────────────────────────────────

class ValueChainStage(BaseModel):
    stage: str
    description: str
    key_players: list[str] = []
    margin_capture: str = ""  # "High" | "Medium" | "Low"
    power_dynamics: str = ""

class ProfitPoolSegment(BaseModel):
    segment: str
    margin_percent: float | None = None
    profitability_tier: str = ""  # "High" | "Medium" | "Low"
    notes: str = ""

class MarketStructure(BaseModel):
    value_chain: list[ValueChainStage] = []
    profit_pools: list[ProfitPoolSegment] = []
    typical_cost_structure: dict[str, str] = {}  # e.g. "COGS" → "45-50%"
    pricing_models: list[str] = []
    capex_intensity: str = ""  # "High" | "Medium" | "Low"
    where_margins_captured: str = ""
    where_power_sits: str = ""

# ── Section 5: Competitive Landscape ─────────────────────────────────────────

class CompetitorEntry(BaseModel):
    name: str
    tier: str  # Leader | Challenger | Niche | Disruptor
    market_share_pct: float | None = None
    revenue_usd_bn: float | None = None
    geographic_reach: str = ""
    key_strengths: list[str] = []

class PositioningMatrixEntry(BaseModel):
    company: str
    x_axis_value: float  # e.g. innovation score 0-10
    y_axis_value: float  # e.g. scale score 0-10
    tier: str

class CompetitiveLandscape(BaseModel):
    overview_narrative: str = ""
    key_players: list[CompetitorEntry] = []
    market_concentration: str = ""  # "Fragmented" | "Moderately concentrated" | "Concentrated"
    positioning_x_axis: str = "Innovation"
    positioning_y_axis: str = "Scale"
    positioning_matrix: list[PositioningMatrixEntry] = []
    strategic_moves: list[str] = []
    new_entrants_disruptors: list[str] = []

# ── Section 6: Customer Analysis ─────────────────────────────────────────────

class CustomerSegment(BaseModel):
    name: str
    description: str
    size_estimate: str = ""
    growth_rate: str = ""

class CustomerAnalysis(BaseModel):
    segments: list[CustomerSegment] = []
    key_purchase_drivers: list[str] = []
    pain_points: list[str] = []
    unmet_needs: list[str] = []
    decision_makers: list[str] = []
    procurement_process: str = ""
    switching_costs: str = ""  # "High" | "Medium" | "Low"
    willingness_to_pay: str = ""
    lifetime_value_notes: str = ""
    price_sensitivity: str = ""  # "High" | "Medium" | "Low"

# ── Section 7: Technology Trends ─────────────────────────────────────────────

class TechTrend(BaseModel):
    technology: str
    description: str
    impact_level: str = ""  # "High" | "Medium" | "Low"
    time_horizon: str = ""  # "Now" | "1-3yr" | "3-5yr"

class RDPlayer(BaseModel):
    company: str
    rd_spend_usd_bn: float | None = None
    rd_as_pct_revenue: float | None = None
    notable_patents: list[str] = []

class TechTrends(BaseModel):
    product_innovations_5yr: list[str] = []
    disruptive_technologies: list[TechTrend] = []
    rd_intensity_notes: str = ""
    rd_leaders: list[RDPlayer] = []
    innovation_pipeline: list[str] = []

# ── Section 8: Regulatory & External ─────────────────────────────────────────

class RegulatoryItem(BaseModel):
    area: str
    description: str
    impact: str = ""  # "High" | "Medium" | "Low"
    region: str = "Global"

class MacroFactor(BaseModel):
    factor: str
    current_state: str
    impact_on_market: str

class ESGItem(BaseModel):
    area: str  # Sustainability | Carbon | Ethical sourcing | Social
    description: str
    regulatory_pressure: str = ""  # "High" | "Medium" | "Low"

class RegulatoryFactors(BaseModel):
    regulations: list[RegulatoryItem] = []
    macro_factors: list[MacroFactor] = []
    esg_trends: list[ESGItem] = []

# ── Section 9: Geographic ─────────────────────────────────────────────────────

class RegionData(BaseModel):
    region: str
    market_size_usd_bn: float | None = None
    share_pct: float | None = None
    cagr_percent: float | None = None
    growth_stage: str = ""  # Emerging | Growing | Mature

class GeographicLandscape(BaseModel):
    regions: list[RegionData] = []
    growth_hotspots: list[str] = []
    local_champion_markets: list[str] = []
    global_vs_local_dynamics: str = ""

# ── Section 10: Investment & M&A ─────────────────────────────────────────────

class Deal(BaseModel):
    deal_type: str  # Acquisition | Merger | Investment | PE | VC
    acquirer: str
    target: str
    value_usd_mn: float | None = None
    date: str = ""
    strategic_rationale: str = ""

class InvestmentMA(BaseModel):
    recent_deals: list[Deal] = []
    pe_themes: list[str] = []
    vc_emerging_startups: list[str] = []
    capital_flow_narrative: str = ""
    total_deal_value_usd_bn: float | None = None

# ── Section 11: Risks ─────────────────────────────────────────────────────────

class Risk(BaseModel):
    category: str  # Regulatory | Technology | Supply Chain | Macro | Competitive
    risk: str
    likelihood: str = ""  # High | Medium | Low
    impact: str = ""      # High | Medium | Low
    mitigation: str = ""

# ── Section 12: Strategic Opportunities ──────────────────────────────────────

class StrategicPlay(BaseModel):
    play_type: str  # New product | Geographic expansion | Acquisition | Partnership
    description: str
    rationale: str
    estimated_impact: str = ""

class StrategicOpportunities(BaseModel):
    white_space_opportunities: list[str] = []
    capability_fit_areas: list[str] = []
    potential_strategic_plays: list[StrategicPlay] = []
    recommended_priorities: list[str] = []

# ── Full Report ───────────────────────────────────────────────────────────────

class MarketScanReport(BaseModel):
    scan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: str
    market: str
    time_period_months: int
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Section 1: Executive Summary
    market_snapshot: MarketSnapshot = Field(default_factory=MarketSnapshot)
    key_insights: list[str] = []
    implications: Implications = Field(default_factory=Implications)
    opportunities_identified: list[str] = []
    exec_summary_bullets: list[str] = []

    # Sections 2-12
    market_definition: MarketDefinition = Field(default_factory=MarketDefinition)
    market_size: MarketSizeData = Field(default_factory=MarketSizeData)
    market_structure: MarketStructure = Field(default_factory=MarketStructure)
    competitive_landscape: CompetitiveLandscape = Field(default_factory=CompetitiveLandscape)
    customer_analysis: CustomerAnalysis = Field(default_factory=CustomerAnalysis)
    tech_trends: TechTrends = Field(default_factory=TechTrends)
    regulatory: RegulatoryFactors = Field(default_factory=RegulatoryFactors)
    geographic: GeographicLandscape = Field(default_factory=GeographicLandscape)
    investment_ma: InvestmentMA = Field(default_factory=InvestmentMA)
    risks: list[Risk] = []
    strategic_opportunities: StrategicOpportunities = Field(default_factory=StrategicOpportunities)

    # Section 13: Appendix
    all_sources: list[SearchResult] = []


class MarketScanJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: Literal["queued", "researching", "synthesizing", "complete", "error"] = "queued"
    progress_message: str = "Starting research..."
    progress_pct: int = 0
    error: str | None = None
    report: MarketScanReport | None = None
