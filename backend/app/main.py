from fastapi import FastAPI

app = FastAPI(
    title="MLForge API",
    description="Backend API for MLForge",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to MLForge 🚀"
    }