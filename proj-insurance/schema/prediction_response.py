from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    
    predicted_category: str = Field(
        ...,
        description="Predicted insurance category",
        examples=["high"]
    )

    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range 0 to 1)",
        examples=[0.95]
    )

    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        examples=[{"low": 0.1, "medium": 0.2, "high": 0.7}]
    )
