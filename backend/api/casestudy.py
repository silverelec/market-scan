import logging, io
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from backend.schemas.request import ScanRequest
from backend.schemas.casestudy import CaseStudyJob
from backend.services.casestudy_builder import build_case_studies

logger = logging.getLogger(__name__)
router = APIRouter()
_jobs: dict[str, CaseStudyJob] = {}


@router.post("/case-study", response_model=CaseStudyJob, status_code=202)
async def start_case_study(body: ScanRequest, background_tasks: BackgroundTasks):
    job = CaseStudyJob()
    _jobs[job.job_id] = job
    background_tasks.add_task(build_case_studies, body, job, _jobs)
    logger.info(f"Case study started: {job.job_id} — {body.company} / {body.market}")
    return job


@router.get("/case-study/{job_id}", response_model=CaseStudyJob)
async def get_case_study(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/case-study/{job_id}/pdf")
async def download_case_study_pdf(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "complete" or not job.report:
        raise HTTPException(status_code=400, detail="Report not yet complete")
    try:
        from backend.pdf.renderer import render_casestudy_pdf
        pdf_bytes = render_casestudy_pdf(job.report)
        filename = f"case-studies-{job.report.company.replace(' ', '-')}-{job.report.market.replace(' ', '-')}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes), media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")
