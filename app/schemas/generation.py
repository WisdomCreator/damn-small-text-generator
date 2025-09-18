from pydantic import BaseModel
from app.enums.generation_status import GenerationStatus
from typing import Any


class Generation(BaseModel):
    gen_id: int
    model_name: str
    status: GenerationStatus
    params: dict[str, Any]
    message: str


class TextGeneration(Generation):
    template_id: int
    veriables: dict[str, Any]
