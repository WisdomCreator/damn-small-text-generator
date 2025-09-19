from fastapi import APIRouter, HTTPException, status
from app.services.llm_models_registry import LLMModelsRegistry
from app.schemas.llm_model import LLMModelStatusResponse, LLMModelListResponse, LLMLoadedModelListResponse

router = APIRouter(prefix="/models", tags=["models"])

llm_registry = LLMModelsRegistry()

@router.get("/", response_model=LLMModelListResponse)
def list_models():
    return {"models": llm_registry.list_all_models()}


@router.get("/loaded")
def list_loaded_models():
    return {"loaded_models": llm_registry.list_loaded_models()}


@router.get("/{model_name}", response_model=LLMModelStatusResponse)
def get_model_status(model_name: str):
    try:
        return {"model_name": model_name, "loaded": llm_registry.is_model_loaded(model_name)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{model_name}/load")
def load_model(model_name: str):
    pass


@router.post("/{model_name}/unload")
def unload_model(model_name: str):
    pass

@router.post("/unload_all_models")
def unload_all_models():
    pass
