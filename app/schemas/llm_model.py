from pydantic import BaseModel
from typing import Optional, List


class LLMModelStatusResponse(BaseModel):
    model_name: str
    loaded: bool


class LLMModelListResponse(BaseModel):
    models: List[str]


class LLMLoadedModelListResponse(BaseModel):
    loaded_models: List[str]


class ModelsQuery(BaseModel):
    loaded: Optional[bool] = None


class LoadLLMModelRequest(BaseModel):
    provider_type: str


class UnloadLLMModelRequest(BaseModel):
    model_name: str


class CreateTaskResponse(BaseModel):
    task_id: str
