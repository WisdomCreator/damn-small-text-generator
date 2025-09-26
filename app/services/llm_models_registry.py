import os
import redis
from typing import Dict, List
from app.services.llm_providers import TorchProvider, MODELS_DIR


class LLMModelsRegistry:
    def __init__(self, redis_url: str) -> None:
        self.__redis = redis.Redis.from_url(redis_url, decode_responses=True)
        self.__loaded_models: Dict[str, TorchProvider] = {}

    def list_all_models(self) -> List[str]:
        return os.listdir(MODELS_DIR)

    def list_loaded_models(self):
        return list(self.__loaded_models.keys())

    def get_loaded_model(self, model_name: str) -> TorchProvider:
        return self.__loaded_models[model_name]

    def load_model_by_name(self, model_name: str):
        llm_provider = TorchProvider(model_name)
        llm_provider.load_model()
        self.__loaded_models[model_name] = llm_provider
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

    def get_model_by_name(self, model_name: str) -> TorchProvider:
        return self.__loaded_models[model_name]

    def is_model_loaded(self, model_name: str) -> bool:
        if self.is_model_exist(model_name):
            return model_name in self.__loaded_models
        raise ValueError(f"Model {model_name} not found")

    def is_model_exist(self, model_name: str) -> bool:
        return model_name in os.listdir(MODELS_DIR)
