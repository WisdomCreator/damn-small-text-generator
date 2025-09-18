from fastapi import APIRouter

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def get_models():
    pass


@router.get("/loaded")
def get_loaded_models():
    pass


@router.get("/{model_name}")
def get_model_status(model_name: str):
    pass


@router.post("/{model_name}/load")
def load_model(model_name: str):
    pass


@router.post("/{model_name}/unload")
def unload_model(model_name: str):
    pass
