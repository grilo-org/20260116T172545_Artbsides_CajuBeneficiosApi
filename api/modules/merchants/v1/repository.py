from typing import Optional
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession

from api.confs.database import mongodb_session
from api.modules.merchants.v1.dtos.merchant import MerchantDto
from api.modules.merchants.v1.entities.merchant import Merchant


async def db_session() -> AsyncIOMotorClientSession: return await mongodb_session(document_models = [
    Merchant
])


class MerchantRepository:
    def __init__(self, db_session: AsyncIOMotorClientSession = Depends(db_session)) -> None:
        self.db_session = db_session

    async def read_one(self, parameters: MerchantDto.ReadOne.Parameters) -> Optional[Merchant]:
        return await Merchant.find_one(
            Merchant.name == parameters.name
        )
