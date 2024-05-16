from abc import ABC, abstractmethod
from typing import Any, Dict


class HttpProviderConnector(ABC):
    @abstractmethod
    def get(self, url: str, headers: Dict[str, str]) -> Any:
        pass

    @abstractmethod
    def post(self, url: str, data: Dict[str, Any], headers: Dict[str, str]) -> Any:
        pass
