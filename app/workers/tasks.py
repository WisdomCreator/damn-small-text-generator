from app.workers.celery_app import celery
from app.db.session import SyncSessionLocal
from app.db.models import Generation
from app.config import get_settings
from app.enums.generation_status import GenerationStatus
from app.services.llm_models_registry import LLMModelsRegistry

settings = get_settings()
llm_registry = LLMModelsRegistry(settings.REDIS_URL + "/2")


@celery.task(name="app.workers.tasks.process_generation", bind=True)
def generation_task(self, generation_id: int, prompt: str, model_name: str, **params):
    db = SyncSessionLocal()
    try:
        generation = db.get(Generation, generation_id)
        if not generation:
            return
        generation.status = GenerationStatus.RUNNING
        db.commit()
        db.refresh(generation)
        if llm_registry.is_model_loaded(model_name):
            llm_provider = llm_registry.get_model_by_name(model_name)
            generation.generated_text = str(llm_provider.generate(prompt, **params))
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
    if generation:
        return {"status": GenerationStatus.SUCCEEDED, "generation_id": generation_id}
    else:
        return {"status": GenerationStatus.FAILED, "generation_id": generation_id}


@celery.task(name="app.workers.tasks.list_models", bind=True)
def list_models_task(self, loaded: bool = False):
    models = (
        llm_registry.list_loaded_models() if loaded else llm_registry.list_all_models()
    )
    return {"status": "succeeded", "models": models}


@celery.task(name="app.workers.tasks.get_model_status", bind=True)
def get_model_status_task(self, model_name: str):
    return {
        "status": "succeeded",
        "model_name": model_name,
        "loaded": llm_registry.is_model_loaded(model_name),
    }


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


@celery.task(name="app.workers.tasks.unload_model", bind=True)
def unload_model_task(self, model_name: str):
    return {
        "status": "succeeded",
        "unloaded": llm_registry.unload_model_by_name(model_name),
    }


@celery.task(name="app.workers.tasks.unload_all_models", bind=True)
def unload_all_models_task(self):
    return {"status": "succeeded", "unloaded_count": llm_registry.unload_all_models()}
