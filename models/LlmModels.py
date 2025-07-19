from enum import Enum
from pydantic  import BaseModel as BM

class LLMMessageRoleEnum(str,Enum):
    user = "user"
    system = "system"

class LLMMessageModel(BM):
    role: LLMMessageRoleEnum
    content:str


class LLMModel(BM):
    messages: list[LLMMessageModel]
    # model: str = "llama3-70b-8192"
    # model: str = "llama3-8b-8192"
    model: str = "mistral-saba-24b"
    temperature: float = 0.7
    maxTokens:int = 4000
    stream:bool=False
    jsonResponse:bool=False