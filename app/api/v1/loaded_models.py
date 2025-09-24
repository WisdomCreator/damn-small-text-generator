from fastapi import APIRouter
from app.schemas.llm_model import CreateTaskResponse
from app.workers.tasks import load_model_task, unload_model_task, unload_all_models_task

router = APIRouter(prefix="/loaded-models", tags=["loaded-models"])

@router.post("/{model_name}", response_model=CreateTaskResponse)
def load_model(model_name: str):
    task = load_model_task.delay(model_name)
    return {"task_id": task.id}


@router.delete("/{model_name}", response_model=CreateTaskResponse)
def unload_model(model_name: str):
    task = unload_model_task.delay(model_name)
    return {"task_id": task.id}

@router.delete("/", response_model=CreateTaskResponse)
def unload_all_models():
    task = unload_all_models_task.delay()
    return {"task_id": task.id}