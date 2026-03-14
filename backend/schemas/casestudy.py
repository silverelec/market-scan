from pydantic import BaseModel, Field
from typing import Literal
import uuid
from datetime import datetime


class CaseStudy(BaseModel):
    number: int  # 1-5
    title: str

    # Section 1: Innovation Overview
    innovation_description: str = ""  # 1-2 sentences what it is
    problem_solved: str = ""
    where_emerging: str = ""

    # Section 2: Example in Practice
    lead_company: str = ""
    implementation_description: str = ""
    metrics_outcomes: list[str] = []

    # Section 3: Impact on the Industry
    customer_impact: str = ""
    business_performance_impact: str = ""
    competitive_dynamics_impact: str = ""

    # Section 4: Key Takeaways
    key_takeaways: list[str] = []  # 3-4 bullets

    # Section 5: Relevance for the Client
    client_relevance: str = ""
    potential_opportunity: str = ""

    # Metadata
    innovation_type: str = ""  # Technology | Business Model | Operations | Customer | ESG
    maturity_level: str = ""   # Emerging | Scaling | Mainstream


class CaseStudyReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: str
    market: str
    time_period_months: int
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    case_studies: list[CaseStudy] = []
    report_narrative: str = ""  # Brief framing paragraph
    all_sources: list[dict] = []


class CaseStudyJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: Literal["queued", "researching", "identifying", "synthesizing", "complete", "error"] = "queued"
    progress_message: str = "Starting research..."
    progress_pct: int = 0
    error: str | None = None
    report: CaseStudyReport | None = None
