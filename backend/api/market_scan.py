import uuid
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
import io

from backend.schemas.request import ScanRequest
from backend.schemas.market_scan import MarketScanJob
from backend.services.market_scan_builder import build_market_scan

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory job store
_jobs: dict[str, MarketScanJob] = {}


@router.post("/market-scan", response_model=MarketScanJob, status_code=202)
async def start_market_scan(body: ScanRequest, background_tasks: BackgroundTasks):
    job = MarketScanJob()
    _jobs[job.job_id] = job
    background_tasks.add_task(build_market_scan, body, job, _jobs)
    logger.info(f"Market scan started: {job.job_id} — {body.company} / {body.market}")
    return job


@router.get("/market-scan/{job_id}", response_model=MarketScanJob)
async def get_market_scan(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan job not found")
    return job


@router.get("/market-scan/{job_id}/pdf")
async def download_market_scan_pdf(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan job not found")
    if job.status != "complete" or not job.report:
        raise HTTPException(status_code=400, detail="Report not yet complete")
    try:
        from backend.pdf.renderer import render_market_scan_pdf
        pdf_bytes = render_market_scan_pdf(job.report)
        filename = f"market-scan-{job.report.company.replace(' ', '-')}-{job.report.market.replace(' ', '-')}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        logger.exception(f"PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")
