from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.generation import GenerationCreateRequest
from app.db.session import get_db
from app.db.models import Generation
from app.workers.tasks import generation_task
from app.enums.generation_status import GenerationStatus

router = APIRouter(prefix="/text-generations", tags=["text_generations"])


@router.post("/")
def create_generation_task(request: GenerationCreateRequest, db: Session = Depends(get_db)):
    generation = Generation(status=GenerationStatus.QUEUED, prompt=request.prompt, model_name=request.model_name)
    db.add(generation)
    db.commit()
    generation_task.delay(generation.id, request.prompt, request.model_name)
    return generation.id


@router.get(
    "/{gen_id}",
    summary="Получить статус генерации по id",
)
def get_text_generation(gen_id: int):
    pass