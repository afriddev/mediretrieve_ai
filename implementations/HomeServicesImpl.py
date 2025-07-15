from abc import ABC,abstractmethod
from fastapi.responses import JSONResponse


class HomeServicesImpl(ABC):
    
    @abstractmethod
    def llmAsk(self,question:str) -> JSONResponse:
        pass 