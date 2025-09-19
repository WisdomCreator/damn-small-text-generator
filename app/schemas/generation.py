from pydantic import BaseModel

class GenerationCreateRequest(BaseModel):
    prompt: str
    model_name: str
    #params: dict[str, Any] = {}
