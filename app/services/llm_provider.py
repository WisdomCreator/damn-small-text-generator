import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from abc import ABC, abstractmethod
from typing import Optional

MODELS_DIR = "models/"


class LLMProvider(ABC):
    def __init__(self, model_name: str):
        self.__model_name = model_name

    @property
    def model_name(self) -> str:
        return self.__model_name

    @abstractmethod
    def generate(self, prompt: str) -> str: ...
    @abstractmethod
    def load_model(self): ...
    @abstractmethod
    def unload_model(self) -> bool: ...


class TorchProvider(LLMProvider):
    def __init__(self, model_name: str, device: Optional[str] = None):
        self.__model_name = model_name
        self.__device = device

        if device:
            self.__device = device
        elif torch.cuda.is_available():
            self.__device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            self.__device = "mps"
        else:
            self.__device = "cpu"
        print(self.__device)

        self.__nlp = None

    def generate(self, prompt: str) -> str:
        if self.__nlp is None:
            raise RuntimeError("Model is not loaded. Call load_model() first.")
        return str(self.__nlp(prompt))

    def load_model(self):
        dtype = torch.float16 if self.__device in ("cuda", "mps") else torch.float32

        tokenizer = AutoTokenizer.from_pretrained(
            MODELS_DIR + self.__model_name,
            torch_dtype=dtype,
        )

        model = AutoModelForCausalLM.from_pretrained(
            MODELS_DIR + self.__model_name,
            torch_dtype=dtype,
            local_files_only=True,
        )

        self.__nlp = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto" if self.__device != "cpu" else None,
        )
        return self.__nlp

    def unload_model(self):
        if self.__nlp is None:
            return False
        
        pipe = self.__nlp
        self.__nlp = None

        try:
            model = getattr(pipe, "model")
            tokenizer = getattr(pipe, "tokenizer")
            # Перед удалением модели изменяем режим работы на cpu, чтобы освободить видеопамять
            if model is not None:
                try:
                    model.cpu()
                except Exception:
                    pass
                del model
            
            if tokenizer is not None:
                del tokenizer
            del pipe
        finally:
            gc.collect()

            if self.__device == "cuda" and torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif self.__device == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
                torch.mps.empty_cache()
        return True
