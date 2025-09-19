from pydantic import BaseModel
from typing import List

class LLMModelStatusResponse(BaseModel):
    model_name: str
    loaded: bool

class LLMModelListResponse(BaseModel):
    models: List[str]

class LLMLoadedModelListResponse(BaseModel):
    loaded_models: List[str]

class LoadLLMModelRequest(BaseModel):
    model_name: str

class UnloadLLMModelRequest(BaseModel):
    model_name: str
    