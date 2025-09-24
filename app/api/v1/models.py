from fastapi import APIRouter, HTTPException, Depends
from app.workers.tasks import list_models_task, get_model_status_task
from app.schemas.llm_model import ModelsQuery, LLMModelStatusResponse, LLMModelListResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=LLMModelListResponse)
def list_models(params: ModelsQuery = Depends()):
    task = list_models_task.delay(params.loaded)
    result = task.get(timeout=5)
    return {"models": result["models"]}


@router.get("/{model_name}", response_model=LLMModelStatusResponse)
def get_model_status(model_name: str):
    try:
        task = get_model_status_task.delay(model_name)
        result = task.get(timeout=5)
        return {"model_name": result["model_name"], "loaded": result["loaded"]}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



