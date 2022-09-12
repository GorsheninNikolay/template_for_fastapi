from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.connection import get_session
from app.schemas import PongResponse
from app.utils.health_check import health_check_db

api_router = APIRouter(tags=['Health check'])


@api_router.get(
    "/ping_application",
    response_model=PongResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_application(
    _: Request,
):
    return {"message": "Application is working!"}


@api_router.get(
    "/ping_database",
    response_model=PongResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Database isn't working"
        }
    },
)
async def ping_database(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    if await health_check_db(session):
        return {"message": "Database is working!"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database isn't working",
    )
