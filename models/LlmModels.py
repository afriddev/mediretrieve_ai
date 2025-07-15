from enum import Enum
from pydantic  import BaseModel as BM

class MessageRoleEnum(str,Enum):
    user = "user"
    system = "system"

class MessageModel(BM):
    role: MessageRoleEnum
    content:str


class LLMModel(BM):
    messages: list[MessageModel]
    model: str = "llama3-70b-8192"
    temperature: float = 0.7
    maxTokens:int = 1024
    stream:bool=False
    jsonResponse:bool=False