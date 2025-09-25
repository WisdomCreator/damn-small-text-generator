from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.generation import CreateTextGenerationRequest, CreateTextGenerationResponse, GetTextGenerationResponse
from app.db.session import get_db
from app.db.models import Generation
from app.workers.tasks import generation_task
from app.enums.generation_status import GenerationStatus

router = APIRouter(prefix="/text-generations", tags=["text_generations"])


@router.post("/", response_model=CreateTextGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_generation_task(request: CreateTextGenerationRequest, db: AsyncSession = Depends(get_db)):
    generation = Generation(status=GenerationStatus.QUEUED, prompt=request.prompt, model_name=request.model_name)
    db.add(generation)
    await db.commit()
    await db.refresh(generation)
    generation_task.delay(generation.id, request.prompt, request.model_name)
    return {"generation_id": generation.id}


@router.get("/{gen_id}", response_model=GetTextGenerationResponse, response_model_exclude_none=True)
async def get_text_generation(gen_id: int, db: AsyncSession = Depends(get_db)):
    generation = await db.get(Generation, gen_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return {"id": generation.id, "status": generation.status, "prompt": generation.prompt, "text": generation.text, "message": generation.message}