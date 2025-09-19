from app.workers.celery_app import celery
from app.db.session import SessionLocal
from app.db.models import Generation
from app.enums.generation_status import GenerationStatus
from app.services.llm_models_registry import LLMModelsRegistry

llm_registry = LLMModelsRegistry()

@celery.task(name="app.workers.tasks.process_generation", bind=True)
def generation_task(self, generation_id: int, prompt: str, model_name: str):
    db = SessionLocal()
    try:
        generation = db.get(Generation, generation_id)
        if not generation:
            return
        generation.status = GenerationStatus.RUNNING
        db.commit()
        db.refresh(generation)
        if llm_registry.is_model_loaded(model_name):
            llm_provider = llm_registry.get_model_by_name(model_name)
            generation.text = str(llm_provider.generate(prompt))
            generation.status = GenerationStatus.SUCCEEDED
        else:
            generation.status = GenerationStatus.FAILED
            generation.message = f"Model {model_name} is not loaded"
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

@celery.task(name="app.workers.tasks.load_model", bind=True)
def load_model_task(self, model_name: str):
    try:
        if llm_registry.is_model_exist(model_name):
            if not llm_registry.is_model_loaded(model_name):
                llm_registry.load_model_by_name(model_name)
                return {"status": "loaded", "model_name": model_name}
            else:
                return {"status": "already loaded", "model_name": model_name}
        else:
            return {"status": "model not found", "model_name": model_name}
    except Exception as e:
        return {"status": "error", "model_name": model_name, "error": str(e)}
