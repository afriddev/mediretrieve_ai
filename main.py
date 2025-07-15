import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from middleware import CustomMidlleware
from controllers.HomeController import homeControllerRouter
from services.LlmModelServcies import LlmModelServcies
from services.EmbeddingServices import EmbeddingServices

mediRetrieveAi = FastAPI()


mediRetrieveAi.add_middleware(
    CORSMiddleware,
    allow_origins=["* "],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@mediRetrieveAi.exception_handler(RequestValidationError)
async def validation_exception_handler():
    return JSONResponse(
        status_code=400,
        content={
            "data": "BAD_REQUEST",
        },
    )


llmModelServices: LlmModelServcies = LlmModelServcies()
embeddingServices: EmbeddingServices = EmbeddingServices()

mediRetrieveAi.add_middleware(CustomMidlleware)
mediRetrieveAi.include_router(homeControllerRouter, prefix="/api/internal")

if __name__ == "__main__":
    uvicorn.run("main:mediRetrieveAi", host="0.0.0.0", port=8000, reload=True)
