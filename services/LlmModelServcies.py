from groq import Groq
import os
from dotenv import load_dotenv
from models.LlmModels import LLMModel
from typing import Any, Dict, cast
from typing import Any, cast

load_dotenv()


class LlmModelServcies:
    llm = cast(Any, Groq(api_key=os.getenv("GROQ_API_KEY")))
    
    @staticmethod
    def callModel( model: LLMModel) -> str:
        params: Dict[str, Any] = {
            "messages": model.messages,
            "model": model.model,
            "max_completion_tokens": model.maxTokens,
            "temperature": model.temperature,
            "stream": model.stream,
        }

        if model.jsonResponse:
            params["response_format"] = {"type": "json_object"}

        response = LlmModelServcies.llm.chat.completions.create(**params)
        return response.choices[0].message.content
