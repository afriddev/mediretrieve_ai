from groq import Groq
import os
from dotenv import load_dotenv
from models.LlmModels import LLMMessageModel, LLMMessageRoleEnum, LLMModel
from typing import Any, Dict, cast
from typing import Any, cast
from utils.EmbeddingServices import EmbeddingServices

load_dotenv()


class LlmModelServcies(EmbeddingServices):

    def __init__(self):
        super().__init__()
        self.llm = cast(Any, Groq(api_key=os.getenv("GROQ_API_KEY")))

    def callModel(self, model: LLMModel) -> str:
        params: Dict[str, Any] = {
            "messages": [msg.model_dump(mode="json") for msg in model.messages],
            "model": model.model,
            "max_completion_tokens": model.maxTokens,
            "temperature": model.temperature,
            "stream": model.stream,
        }

        if model.jsonResponse:
            params["response_format"] = {"type": "json_object"}

        response = self.llm.chat.completions.create(**params)
        return response.choices[0].message.content

    def extarctMedicalSchemeJson(self):
        text = self.extarctTextFromPdfFile()
        modelResponse = self.callModel(
            model=LLMModel(
                jsonResponse=True,
                temperature=0,
                messages=[
                    LLMMessageModel(
                        role=LLMMessageRoleEnum.system,
                        content="""
You are a helpful AI assistant — For each treatment type, write a detailed regularEmbeddingText of 2-3 sentences starting with its name and describing common procedures, purposes, and related care. Mention the treatment name in multiple ways inside the text to improve search results. Write a shortEmbeddingText starting with the treatment name, followed by key procedures in 6-8 words. Do not include price inside the texts. Output valid JSON like {"data":[{"title":"Dental Treatment","price":"10000","regularEmbeddingText":"Dental treatment includes fillings, root canal, tooth cleaning, crowns, and extractions. Dental care covers regular cleaning, cavity treatments, and gum care. Dental procedures help maintain oral health and prevent infections.","shortEmbeddingText":"Dental treatment: fillings, root canal, crowns"}]}. Return only the JSON. Make sure JSON is valid with no extra characters.


""",
                    ),
                    LLMMessageModel(
                        role=LLMMessageRoleEnum.user,
                        content=text,
                    ),
                ],
            )
        )
        print(modelResponse)
