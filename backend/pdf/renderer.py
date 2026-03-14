"""
PDF renderer using WeasyPrint + Jinja2.
Falls back gracefully if WeasyPrint is not available.
"""

import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"


def _get_jinja_env() -> Environment:
    return Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)


def _render_html(template_name: str, context: dict) -> str:
    env = _get_jinja_env()
    template = env.get_template(template_name)
    return template.render(**context)


def _html_to_pdf(html: str) -> bytes:
    """Try WeasyPrint, then xhtml2pdf (pure-Python), then pdfkit."""
    try:
        from weasyprint import HTML
        return HTML(string=html).write_pdf()
    except ImportError:
        logger.warning("WeasyPrint not available, trying xhtml2pdf")
    except Exception as e:
        logger.warning(f"WeasyPrint failed: {e}, trying xhtml2pdf")

    try:
        import io
        from xhtml2pdf import pisa
        buf = io.BytesIO()
        result = pisa.CreatePDF(html.encode("utf-8"), dest=buf, encoding="utf-8")
        if not result.err:
            return buf.getvalue()
        logger.warning(f"xhtml2pdf reported errors, trying pdfkit")
    except ImportError:
        logger.warning("xhtml2pdf not available, trying pdfkit")
    except Exception as e:
        logger.warning(f"xhtml2pdf failed: {e}, trying pdfkit")

    try:
        import pdfkit
        return pdfkit.from_string(html, False)
    except Exception as e:
        logger.error(f"pdfkit also failed: {e}")
        raise RuntimeError(f"PDF generation unavailable: {e}") from e


def render_market_scan_pdf(report) -> bytes:
    from backend.pdf import charts

    # Generate charts
    chart_tam = charts.tam_sam_som_chart(
        report.market_size.tam_usd_bn,
        report.market_size.sam_usd_bn,
        report.market_size.som_usd_bn,
    )
    chart_growth = charts.market_growth_chart(
        [d.model_dump() for d in report.market_size.historical_data],
        [d.model_dump() for d in report.market_size.forecast_data],
    )
    chart_regional = charts.regional_bar_chart(
        [r.model_dump() for r in report.geographic.regions]
    )
    chart_share = charts.market_share_pie(
        [p.model_dump() for p in report.competitive_landscape.key_players]
    )

    html = _render_html("market_scan.html", {
        "report": report,
        "chart_tam": chart_tam,
        "chart_growth": chart_growth,
        "chart_regional": chart_regional,
        "chart_share": chart_share,
    })
    return _html_to_pdf(html)


def render_competitor_pdf(report) -> bytes:
    from backend.pdf import charts

    chart_radar = charts.capability_radar_chart(
        [r.model_dump() for r in report.benchmarking.capability_benchmark],
        [r.company for r in report.benchmarking.capability_benchmark],
    )
    chart_share = charts.market_share_pie(
        [{"name": r.company, "market_share_pct": r.market_share_pct}
         for r in report.benchmarking.market_share_comparison],
    )

    html = _render_html("competitor.html", {
        "report": report,
        "chart_radar": chart_radar,
        "chart_share": chart_share,
    })
    return _html_to_pdf(html)


def render_casestudy_pdf(report) -> bytes:
    html = _render_html("casestudy.html", {"report": report})
    return _html_to_pdf(html)
