from fastapi import Depends
from datetime import datetime, timezone
from beanie.exceptions import DocumentNotFound
from motor.motor_asyncio import AsyncIOMotorClientSession

from api.confs.database import mongodb_session
from api.modules.accounts.v1.dtos.account import AccountDto
from api.modules.accounts.v1.entities.account import Account


async def db_session() -> AsyncIOMotorClientSession: return await mongodb_session(document_models=[
    Account
])


class AccountRepository:
    def __init__(self, db_session: AsyncIOMotorClientSession = Depends(db_session)) -> None:
        self.db_session = db_session

    async def read_one(self, parameters: AccountDto.ReadOne.Parameters) -> Account:
        if not (account := await Account.find_one(Account.id == parameters.id)):
            raise DocumentNotFound

        return account

    async def update(self, parameters: AccountDto.ReadOne.Parameters, data: AccountDto.Update.Data) -> Account:
        account = await self.read_one(parameters)

        return await account.set({
            **data.model_dump(exclude_unset=True), Account.updated_at: datetime.now(timezone.utc)}, session=self.db_session
        )
