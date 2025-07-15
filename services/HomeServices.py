from implementations.HomeServicesImpl import HomeServicesImpl
from fastapi.responses import JSONResponse
from models.LlmModels import LLMMessageModel, LLMMessageRoleEnum, LLMModel
from services.LlmModelServcies import LlmModelServcies


class HomeServices(HomeServicesImpl):

    def llmAsk(self, question: str) -> JSONResponse:
        answer = LlmModelServcies.callModel(
            LLMModel(
                messages=[
                    LLMMessageModel(role=LLMMessageRoleEnum.user, content=question)
                ]
            )
        )

        return JSONResponse(
            status_code=200,
            content={
                "data": {
                    "question": question,
                    "answer": answer,
                }
            },
        )
