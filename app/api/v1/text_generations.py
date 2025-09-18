from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.generation import TextGeneration
from app.db.session import get_db
from app.db.models import Generation
from app.workers.tasks import process_generation
from app.enums.generation_status import GenerationStatus

router = APIRouter(prefix="/text_generations", tags=["text_generations"])


@router.post("/create")
def create_generation_task(db: Session = Depends(get_db)):
    generation = Generation(status=GenerationStatus.QUEUED)
    db.add(generation)
    db.commit()
    process_generation.delay(generation.id)
    return "true"


@router.get(
    "/{gen_id}",
    response_model=TextGeneration,
    summary="Получить информацию о генерации по id",
)
def get_generation_status(gen_id: int):
    pass


@router.get("/{gen_id}/result")
def get_generation_result(gen_id: int):
    pass
