from fastapi import APIRouter
from services.HomeServices import HomeServices


homeControllerRouter = APIRouter()
homeServices:HomeServices = HomeServices()


@homeControllerRouter.get("/ask/{question}")
def askQuestion(question:str):
    response = homeServices.llmAsk(question=question)
    return response