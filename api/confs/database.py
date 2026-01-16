from beanie import init_beanie
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from api.confs.settings import settings


async def mongodb_session(document_models: Optional[list] = None) -> AsyncIOMotorClientSession:
    client = AsyncIOMotorClient(f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}{settings.DATABASE_PARAMETERS}")

    if document_models:
        await init_beanie(
            database=client[settings.DATABASE_NAME], document_models=document_models
        )

    return await client.start_session()
