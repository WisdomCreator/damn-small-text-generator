import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from app.workers.tasks import list_models_task, get_model_status_task
from app.schemas.llm_model import (
    ModelsQuery,
    LLMModelStatusResponse,
    LLMModelListResponse,
)
from celery.exceptions import TimeoutError  # type: ignore[import-untyped]


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=LLMModelListResponse)
async def list_models(params: ModelsQuery = Depends()):
    task = list_models_task.delay(params.loaded)
    try:
        result = await asyncio.to_thread(task.get, timeout=5)
        return {"models": result["models"]}
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out"
        )


@router.get("/{model_name}", response_model=LLMModelStatusResponse)
async def get_model_status(model_name: str):
    task = get_model_status_task.delay(model_name)
    try:
        result = await asyncio.to_thread(task.get, timeout=5)
        return {"model_name": result["model_name"], "loaded": result["loaded"]}
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out"
        )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
