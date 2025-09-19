from pydantic import BaseModel
from typing import List

class LLMModelStatusResponse(BaseModel):
    model_name: str
    loaded: bool

class LLMModelListResponse(BaseModel):
    models: List[str]

class LLMLoadedModelListResponse(BaseModel):
    loaded_models: List[str]

    