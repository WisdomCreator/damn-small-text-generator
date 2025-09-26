from pydantic import BaseModel, Field


class CreateTextGenerationRequest(BaseModel):
    prompt: str
    model_name: str
    max_new_tokens: int = Field(
        default=128, ge=1, description="Maximum number of new tokens"
    )
    temperature: float = Field(default=0.7, ge=0.0, description="Sampling temperature")
    top_k: int = Field(default=50, ge=0, description="Top-K sampling(0 = disabled)")
    top_p: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Top-P (nucleus) sampling"
    )
    repetition_penalty: float = Field(
        default=1.0, ge=1.0, description="Repetition penalty(1.0 = disabled)"
    )
    do_sample: bool = Field(
        default=True,
        description="Whether to use sampling; use greedy decoding otherwise",
    )


class CreateTextGenerationResponse(BaseModel):
    generation_id: int


class GetTextGenerationResponse(BaseModel):
    id: int
    status: str
    prompt: str
    params: dict
    generated_text: str | None = None
    message: str | None = None
