from fastapi import APIRouter

from .endpoints import initiate_analysis
from .endpoints import get_status
from .endpoints import get_result

api_router = APIRouter()


api_router.include_router(
    initiate_analysis.router,
    prefix="/analysis",
    tags=["1. Initiate Analysis"]
)

api_router.include_router(
    get_status.router,
    prefix="/status",
    tags=["2. Check Status"]
)

api_router.include_router(
    get_result.router,
    prefix="/result",
    tags=["3. Get Result"]
)