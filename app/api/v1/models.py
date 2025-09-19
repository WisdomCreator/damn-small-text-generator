from fastapi import APIRouter, HTTPException, status
from app.workers.tasks import load_model_task
from app.schemas.llm_model import LLMModelStatusResponse, LLMModelListResponse, LLMLoadedModelListResponse, LoadLLMModelRequest, UnloadLLMModelRequest

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=LLMModelListResponse)
def list_models():
    return {"models": None}


@router.get("/loaded", response_model=LLMLoadedModelListResponse)
def list_loaded_models():
    return {"loaded_models": None}


@router.get("/{model_name}", response_model=LLMModelStatusResponse)
def get_model_status(model_name: str):
    try:
        return {"model_name": model_name, "loaded": None}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/load")
def load_model(request: LoadLLMModelRequest):
    task = load_model_task.delay(request.model_name)
    return {"task_id": task.id}


@router.post("/unload")
def unload_model(request: UnloadLLMModelRequest):
    pass

@router.post("/unload_all_models")
def unload_all_models():
    pass
