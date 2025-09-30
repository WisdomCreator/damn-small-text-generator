import os
from typing import Dict, List
from app.services.llm_providers import MODELS_DIR, LLMProviderType, LLMProvider, LLMProviderFactory


class LLMModelsRegistry:
    def __init__(self) -> None:
        self.__loaded_models: Dict[str, LLMProvider] = {}

    def list_all_models(self) -> List[str]:
        return [
            model_name
            for model_name in os.listdir(MODELS_DIR)
            if os.path.isdir(os.path.join(MODELS_DIR, model_name))
        ]

    def list_loaded_models(self):
        return list(self.__loaded_models.keys())

    def get_loaded_model(self, model_name: str) -> LLMProvider:
        return self.__loaded_models[model_name]

    def load_model_by_name(self, model_name: str, provider_type: LLMProviderType):
        llm_provider = LLMProviderFactory.create(model_name, provider_type)
        llm_provider.load_model()
        self.__loaded_models[model_name] = llm_provider

    def unload_model_by_name(self, model_name: str) -> bool:
        model = self.__loaded_models.pop(model_name, None)
        if model:
            return model.unload_model()
        return False

    def unload_all_models(self) -> int:
        for model in self.__loaded_models.values():
            model.unload_model()
        count = len(self.__loaded_models)
        self.__loaded_models = {}
        return count

    def is_model_loaded(self, model_name: str) -> bool:
        if self.is_model_exist(model_name):
            return model_name in self.__loaded_models
        raise ValueError(f"Model {model_name} not found")

    def is_model_exist(self, model_name: str) -> bool:
        return os.path.isdir(os.path.join(MODELS_DIR, model_name))
