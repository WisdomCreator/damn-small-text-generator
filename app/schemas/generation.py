from pydantic import BaseModel

class CreateTextGenerationRequest(BaseModel):
    prompt: str
    model_name: str

class CreateTextGenerationResponse(BaseModel):
    generation_id: int

class GetTextGenerationResponse(BaseModel):
    id: int
    status: str
    prompt: str
    text: str | None = None
    message: str | None = None
