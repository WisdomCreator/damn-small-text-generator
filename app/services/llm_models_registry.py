import os
from typing import Dict, List
from app.services.llm_provider import LLMProvider, MODELS_DIR


class LLMModelsRegistry:
    def __init__(self) -> None:
        self.__loaded_models: Dict[str, LLMProvider] = {}

    def list_all_models(self) -> List[str]:
        return os.listdir(MODELS_DIR)

    def list_loaded_models(self):
        return list(self.__loaded_models.keys())

    def get_loaded_model(self, model_name: str) -> LLMProvider:
        return self.__loaded_models[model_name]

    def load_model_by_name(self, llm_provider: LLMProvider):  # изменить на имя
        llm_provider.load_model()
        self.__loaded_models[llm_provider.model_name] = llm_provider
        return llm_provider

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


llm_registry = LLMModelsRegistry()
print(llm_registry.list_all_models())
