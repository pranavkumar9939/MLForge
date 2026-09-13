import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.routes import router
from app.database.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mlforge")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health", tags=["System"])
def health_check():
    """Basic liveness/readiness check for deployment platforms and monitoring."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Never leak raw stack traces to the client. Log the full detail on the
    backend and return a generic, understandable error message instead.
    """
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Something went wrong while processing your request. "
                       "Please try again, and contact support if the problem persists."
        },
    )


# Uploading datasets

from app.api.upload import router as upload_router
from app.api.predict import router as predict_router
from app.api.models import router as models_router
from app.api.compare import router as compare_router
from app.api.feature_importance import router as feature_importance_router
from app.api.roc import router as roc_router
from app.api.confusion_matrix import router as confusion_router
from app.api.datasets import router as datasets_router
from app.api.metrics import router as metrics_router
from app.api.leaderboard import router as leaderboard_router
from app.api.tuning import router as tuning_router
from app.api.model_registry import router as registry_router
from app.api.prediction_history import router as prediction_history_router
from app.api.jobs import router as jobs_router
from app.api.export import router as export_router
from app.api.batch_predict import router as batch_predict_router
from app.api.unsupervised import router as unsupervised_router
from app.api.report import router as report_router
from app.api.auth import router as auth_router


app.include_router(router)
app.include_router(upload_router)
app.include_router(predict_router)
app.include_router(models_router)
app.include_router(compare_router)
app.include_router(feature_importance_router)
app.include_router(roc_router, prefix="/roc", tags=["ROC Curve"])
app.include_router(confusion_router, prefix="/confusion-matrix", tags=["Confusion Matrix"])
app.include_router(datasets_router)
app.include_router(metrics_router)
app.include_router(leaderboard_router)
app.include_router(tuning_router)
app.include_router(registry_router)
app.include_router(prediction_history_router)
app.include_router(jobs_router)
app.include_router(export_router)
app.include_router(batch_predict_router)
app.include_router(unsupervised_router)
app.include_router(report_router)
app.include_router(auth_router)