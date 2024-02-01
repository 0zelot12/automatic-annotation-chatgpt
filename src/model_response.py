from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class ModelResponse(BaseModel):
    """Specifies the expected structure of the model-response to be parsed by langchain."""

    data: List[str] = Field(
        description="Array of strings containing the annotation results"
    )
