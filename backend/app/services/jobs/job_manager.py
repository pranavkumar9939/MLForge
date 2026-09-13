"""
Lightweight in-memory job manager for tracking long-running training runs.

This gives the frontend real, backend-driven progress ("Training Random
Forest (3/8)...") instead of a decorative spinner - every message reported
here corresponds to an actual stage the trainer is executing.

In-memory is a deliberate, simple choice appropriate for a single-process
deployment of this project. If MLForge is ever deployed with multiple
worker processes, this should move to Redis or the database instead.
"""

import threading
import uuid
from datetime import datetime
from typing import Any, Optional

_jobs: dict[str, dict[str, Any]] = {}
_lock = threading.Lock()


def create_job(owner_id: int | None = None) -> str:
    job_id = str(uuid.uuid4())
    with _lock:
        _jobs[job_id] = {
            "job_id": job_id,
            "owner_id": owner_id,
            "status": "pending",  # pending | running | completed | failed
            "stage": "Queued",
            "progress": 0,          # 0-100
            "current_step": 0,
            "total_steps": 0,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
    return job_id


def update_job(job_id: str, **fields) -> None:
    with _lock:
        if job_id not in _jobs:
            return
        _jobs[job_id].update(fields)
        _jobs[job_id]["updated_at"] = datetime.now().isoformat()


def set_progress(job_id: str, stage: str, current_step: int, total_steps: int) -> None:
    progress = int((current_step / total_steps) * 100) if total_steps else 0
    update_job(
        job_id,
        status="running",
        stage=stage,
        current_step=current_step,
        total_steps=total_steps,
        progress=min(progress, 99),  # reserve 100 for true completion
    )


def complete_job(job_id: str, result: dict) -> None:
    update_job(job_id, status="completed", stage="Completed", progress=100, result=result)


def fail_job(job_id: str, error: str) -> None:
    update_job(job_id, status="failed", stage="Failed", error=error)


def get_job(job_id: str) -> Optional[dict]:
    with _lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None
