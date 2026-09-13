from fastapi import APIRouter, Depends, HTTPException

from app.services.jobs import job_manager
from app.core.deps import get_current_user
from app.database.models import User

router = APIRouter(prefix="/jobs", tags=["Jobs"], dependencies=[Depends(get_current_user)])


@router.get("/{job_id}")
def get_job_status(job_id: str, current_user: User = Depends(get_current_user)):
    """
    Poll the status of a background training job. Every field here reflects
    real backend state - `stage`/`progress` are only updated when the
    trainer actually starts/finishes training a specific model.

    Scoped to the job's owner: a valid job_id created by another user
    returns 404, same as every other ownership check in the API.
    """
    job = job_manager.get_job(job_id)

    if job is None or (job.get("owner_id") is not None and job["owner_id"] != current_user.id):
        raise HTTPException(status_code=404, detail="Job not found.")

    return job
