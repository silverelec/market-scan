import logging, io
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from backend.schemas.request import ScanRequest
from backend.schemas.competitor import CompetitorJob
from backend.services.competitor_builder import build_competitor_analysis

logger = logging.getLogger(__name__)
router = APIRouter()
_jobs: dict[str, CompetitorJob] = {}


@router.post("/competitor", response_model=CompetitorJob, status_code=202)
async def start_competitor_analysis(body: ScanRequest, background_tasks: BackgroundTasks):
    job = CompetitorJob()
    _jobs[job.job_id] = job
    background_tasks.add_task(build_competitor_analysis, body, job, _jobs)
    logger.info(f"Competitor analysis started: {job.job_id} — {body.company} / {body.market}")
    return job


@router.get("/competitor/{job_id}", response_model=CompetitorJob)
async def get_competitor_analysis(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/competitor/{job_id}/pdf")
async def download_competitor_pdf(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "complete" or not job.report:
        raise HTTPException(status_code=400, detail="Report not yet complete")
    try:
        from backend.pdf.renderer import render_competitor_pdf
        pdf_bytes = render_competitor_pdf(job.report)
        filename = f"competitor-analysis-{job.report.company.replace(' ', '-')}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes), media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")
