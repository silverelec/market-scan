from pydantic import BaseModel, Field
from typing import Literal
import uuid
from datetime import datetime


# ── Competitor Profile (10 sub-sections) ─────────────────────────────────────

class CompetitorProfile(BaseModel):
    name: str
    is_user_specified: bool = False

    # 3.X.1 Company Overview
    hq: str = ""
    founded: str = ""
    geographic_footprint: list[str] = []
    revenue_usd_bn: float | None = None
    revenue_growth_pct: float | None = None
    market_share_pct: float | None = None
    employee_count: str = ""
    public_private: str = ""  # Public | Private | PE-backed

    # 3.X.2 Business Model
    revenue_streams: list[str] = []
    pricing_model: str = ""
    profit_drivers: list[str] = []
    cost_structure_summary: str = ""

    # 3.X.3 Product & Service Portfolio
    core_offerings: list[str] = []
    differentiators: list[str] = []
    technology_capabilities: list[str] = []
    innovation_pipeline: list[str] = []

    # 3.X.4 Customer Segments
    core_customer_segments: list[str] = []
    industry_focus: list[str] = []
    geographic_focus: list[str] = []
    key_accounts: list[str] = []

    # 3.X.5 Go-To-Market
    sales_model: str = ""
    distribution_channels: list[str] = []
    brand_positioning: str = ""
    customer_acquisition: str = ""

    # 3.X.6 Strategic Moves
    recent_acquisitions: list[str] = []
    product_launches: list[str] = []
    strategic_partnerships: list[str] = []
    geographic_expansion: list[str] = []

    # 3.X.7 Financial Performance
    revenue_trend: str = ""
    profitability_trend: str = ""
    rd_investment: str = ""
    financial_strength: str = ""  # Strong | Moderate | Weak

    # 3.X.8 Strengths & Weaknesses
    strengths: list[str] = []
    weaknesses: list[str] = []
    operational_strengths: list[str] = []

    # 3.X.9 Market Perception
    customer_sentiment: str = ""
    industry_reputation: str = ""
    brand_perception: str = ""
    notable_reviews: list[str] = []

    # 3.X.10 Threat Assessment
    threat_level: str = ""  # High | Medium | Low
    strongest_competition_areas: list[str] = []
    future_risk_potential: str = ""


# ── Benchmarking ─────────────────────────────────────────────────────────────

class CapabilityBenchmarkRow(BaseModel):
    company: str
    product_performance: str = ""     # Leading | Strong | Average | Weak
    innovation_technology: str = ""
    brand_strength: str = ""
    pricing_competitiveness: str = ""
    distribution_reach: str = ""
    partnerships_ecosystem: str = ""
    customer_experience: str = ""

class FeatureMatrixRow(BaseModel):
    feature: str
    scores: dict[str, str]  # company → Present | Partial | Absent

class PricingBenchmarkRow(BaseModel):
    company: str
    pricing_tier: str  # Premium | Mid-market | Value
    pricing_model: str
    relative_value: str  # High | Medium | Low

class MarketShareRow(BaseModel):
    company: str
    market_share_pct: float | None = None
    revenue_usd_bn: float | None = None
    yoy_growth_pct: float | None = None

class SentimentRow(BaseModel):
    company: str
    overall_sentiment: str  # Positive | Neutral | Negative
    key_themes: list[str] = []

class PositioningPoint(BaseModel):
    company: str
    x_value: float  # 0-10
    y_value: float  # 0-10
    is_client: bool = False

class Benchmarking(BaseModel):
    capability_benchmark: list[CapabilityBenchmarkRow] = []
    feature_matrix: list[FeatureMatrixRow] = []
    pricing_benchmark: list[PricingBenchmarkRow] = []
    market_share_comparison: list[MarketShareRow] = []
    sentiment_benchmark: list[SentimentRow] = []
    positioning_x_axis: str = "Innovation"
    positioning_y_axis: str = "Market Reach"
    positioning_map: list[PositioningPoint] = []


# ── Cross-Competitor Analysis ─────────────────────────────────────────────────

class CrossCompetitorAnalysis(BaseModel):
    competitive_battlegrounds: list[str] = []
    client_capability_gaps: list[str] = []
    client_capability_leads: list[str] = []
    emerging_trends: list[str] = []
    common_strategic_themes: list[str] = []
    industry_investment_direction: str = ""


# ── White Spaces ──────────────────────────────────────────────────────────────

class WhiteSpace(BaseModel):
    category: str  # Customer | Product | Geographic | Innovation
    description: str
    attractiveness: str  # High | Medium | Low
    rationale: str


# ── Strategic Recommendations ─────────────────────────────────────────────────

class StrategicRecommendation(BaseModel):
    action: str
    rationale: str
    time_horizon: str  # Immediate | 1-2yr | 3-5yr
    expected_impact: str


class CompetitorReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: str
    market: str
    time_period_months: int
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Section 1: Executive Summary
    purpose: str = ""
    key_findings: list[str] = []
    strategic_implications: list[str] = []

    # Section 2: Market Overview
    industry_overview: str = ""
    industry_structure_summary: str = ""
    competitive_landscape_overview: str = ""
    positioning_x_axis: str = "Innovation"
    positioning_y_axis: str = "Market Reach"
    market_positioning_map: list[PositioningPoint] = []

    # Section 3: Competitor Deep-Dives
    competitors: list[CompetitorProfile] = []

    # Section 4: Benchmarking
    benchmarking: Benchmarking = Field(default_factory=Benchmarking)

    # Section 5: Cross-Competitor Analysis
    cross_competitor: CrossCompetitorAnalysis = Field(default_factory=CrossCompetitorAnalysis)

    # Section 6: White Spaces
    white_spaces: list[WhiteSpace] = []

    # Section 7: Strategic Implications
    competitive_threats: list[str] = []
    competitive_advantages: list[str] = []
    strategic_risks: list[str] = []

    # Section 8: Recommendations
    defend: list[StrategicRecommendation] = []
    differentiate: list[StrategicRecommendation] = []
    expand: list[StrategicRecommendation] = []
    strategic_priorities: list[str] = []

    # Section 9: Appendix
    all_sources: list[dict] = []
    identified_competitors: list[str] = []


class CompetitorJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: Literal["queued", "identifying", "researching", "synthesizing", "complete", "error"] = "queued"
    progress_message: str = "Starting analysis..."
    progress_pct: int = 0
    error: str | None = None
    report: CompetitorReport | None = None
