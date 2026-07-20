from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title = "MLForge API",
    version = "1.0.0"
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploading datasets

from app.api.upload import router as upload_router
from app.api.predict import router as predict_router

app.include_router(router)
app.include_router(upload_router)
app.include_router(predict_router)

