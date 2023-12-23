from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class ModelResponse(BaseModel):
    result: List[str] = Field(
        description="Array of strings containing the annotation results"
    )
