import torch
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
        pass
