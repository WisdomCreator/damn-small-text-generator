from app.workers.celery_app import celery
from app.db.session import SessionLocal
from app.db.models import Generation
from app.services.llm_provider import TorchProvider
from app.enums.generation_status import GenerationStatus


@celery.task(name="app.workers.tasks.process_generation", bind=True)
def process_generation(self, generation_id: int):
    db = SessionLocal()
    try:
        generation = db.get(Generation, generation_id)
        if not generation:
            return
        generation.status = GenerationStatus.RUNNING
        db.commit()
        db.refresh(generation)
        torch_provider = TorchProvider("Qwen3-0.6B")
        torch_provider.load_model()
        generation.text = str(torch_provider.generate("Это тестовая генерация"))
        generation.status = GenerationStatus.SUCCEEDED
        db.commit()
    except Exception as e:
        generation = db.get(Generation, generation_id)
        if generation:
            generation.status = GenerationStatus.FAILED
            generation.message = f"Error: {e}"
            db.commit()
    finally:
        db.close()

    return {"status": "succeeded", "generation_id": generation_id}
