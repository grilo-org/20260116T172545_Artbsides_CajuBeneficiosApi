from typing import Optional
from fastapi import Depends

from api.modules.merchants.v1.repository import MerchantRepository
from api.modules.merchants.v1.dtos.merchant import MerchantDto
from api.modules.merchants.v1.entities.merchant import Merchant


class MerchantService:
    def __init__(self, merchant_repository: MerchantRepository = Depends()) -> None:
        self.merchant_repository = merchant_repository

    async def read_one(self, parameters: MerchantDto.ReadOne.Parameters) -> Optional[Merchant]:
        return await self.merchant_repository.read_one(parameters)
