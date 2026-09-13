"""
Centralized application configuration for MLForge.

All environment-dependent values (paths, CORS origins, upload limits,
training limits) live here instead of being hardcoded across the codebase.
Values can be overridden via environment variables or a `.env` file in the
backend root, without touching any code.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


# Resolve the backend root directory (.../backend/backend)
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- General ---
    APP_NAME: str = "MLForge"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production

    # --- Storage locations ---
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    SAVED_MODELS_DIR: Path = BASE_DIR / "saved_models"
    BATCH_RESULTS_DIR: Path = BASE_DIR / "batch_results"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'mlforge.db'}"

    # --- CORS ---
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
    ]

    # --- Upload limits / security ---
    MAX_UPLOAD_SIZE_MB: int = 200
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls"]

    # --- Dataset / training safety limits ---
    MIN_ROWS_REQUIRED: int = 20
    MAX_ROWS_FOR_FULL_ALGORITHM_SWEEP: int = 50_000
    MAX_ROWS_FOR_EXPENSIVE_MODELS: int = 200_000  # SVM/KNN/kernel methods skipped above this
    MAX_CARDINALITY_FOR_ONEHOT: int = 50
    MAX_BATCH_PREDICTION_ROWS: int = 5000

    # --- Hyperparameter tuning ---
    TUNING_MODE_ITER: dict = {"fast": 5, "balanced": 10, "thorough": 25}
    TUNING_MODE_CV: dict = {"fast": 3, "balanced": 3, "thorough": 5}

    CROSS_VALIDATION_FOLDS: int = 5

    # --- Explainability ---
    SHAP_BACKGROUND_SAMPLE_SIZE: int = 100
    SHAP_MAX_ROWS_FOR_KERNEL_EXPLAINER: int = 50

    # --- Auth ---
    SECRET_KEY: str = "dev-only-insecure-secret-change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_ALGORITHM: str = "HS256"

    def ensure_directories(self) -> None:
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

        if self.DATABASE_URL.startswith("sqlite"):
            # sqlite:///relative/path.db or sqlite:////absolute/path.db -
            # SQLAlchemy/SQLite won't create the parent directory itself.
            db_path = self.DATABASE_URL.split("sqlite:///")[-1]
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.BATCH_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
