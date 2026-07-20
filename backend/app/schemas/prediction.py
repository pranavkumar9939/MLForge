from pydantic import BaseModel
from typing import Dict, Any

class PredictionRequest(BaseModel):

    features : Dict[str, Any]