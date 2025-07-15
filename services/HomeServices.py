from implementations.HomeServicesImpl import HomeServicesImpl

from fastapi.responses import JSONResponse
from models.LlmModels import LLMModel, MessageModel, MessageRoleEnum
from llm.llm import callModel


class HomeServices(HomeServicesImpl):

    def llmAsk(self, question: str) -> JSONResponse:

        answer = callModel(
            LLMModel(
                messages=[MessageModel(role=MessageRoleEnum.user, content=question)]
            )
        )
        return JSONResponse(
            status_code=200,
            content={"data": {"question": question, "answer": answer}},
        )
