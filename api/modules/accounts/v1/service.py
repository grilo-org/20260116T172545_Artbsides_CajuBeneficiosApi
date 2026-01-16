from fastapi import Depends

from api.modules.accounts.v1.repository import AccountRepository
from api.modules.accounts.v1.dtos.account import AccountDto
from api.modules.accounts.v1.entities.account import Account


class AccountService:
    def __init__(self, account_repository: AccountRepository = Depends()) -> None:
        self.account_repository = account_repository

    async def read_one(self, parameters: AccountDto.ReadOne.Parameters) -> Account:
        return await self.account_repository.read_one(parameters)

    async def update(self, parameters: AccountDto.ReadOne.Parameters, data: AccountDto.Update.Data) -> Account:
        return await self.account_repository.update(parameters, data)
