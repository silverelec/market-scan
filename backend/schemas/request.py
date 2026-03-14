from pydantic import BaseModel, Field, field_validator
from typing import Literal


class ScanRequest(BaseModel):
    """Shared input schema for all three features."""
    company: str = Field(..., min_length=1, max_length=200, description="Client company name")
    market: str = Field(..., min_length=1, max_length=300, description="Market or industry to research")
    time_period_months: int = Field(
        default=24,
        ge=1,
        le=120,
        description="How far back to search (1–120 months, default 24 = 2 years)",
    )
    additional_competitors: list[str] = Field(
        default_factory=list,
        description="Optional: specific competitor names to include (Competitor Analysis only)",
    )

    @field_validator("additional_competitors", mode="before")
    @classmethod
    def clean_competitors(cls, v):
        if isinstance(v, str):
            # Handle comma-separated string from form
            return [c.strip() for c in v.split(",") if c.strip()]
        return [c.strip() for c in (v or []) if c.strip()]

    @property
    def tavily_days(self) -> int:
        return self.time_period_months * 30

    @property
    def date_range_label(self) -> str:
        """Human-readable date range for Claude prompts."""
        from datetime import date, timedelta
        end = date.today()
        start = end - timedelta(days=self.tavily_days)
        return f"{start.strftime('%B %Y')} to {end.strftime('%B %Y')}"

    @property
    def exa_start_date(self) -> str:
        """ISO date string for Exa start_published_date parameter."""
        from datetime import date, timedelta
        start = date.today() - timedelta(days=self.tavily_days)
        return start.isoformat()
