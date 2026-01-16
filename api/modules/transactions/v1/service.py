from fastapi import Depends

from api.modules.accounts.v1.service import AccountService
from api.modules.merchants.v1.service import MerchantService
from api.modules.accounts.v1.dtos.account import AccountDto
from api.modules.merchants.v1.dtos.merchant import MerchantDto
from api.modules.transactions.v1.dtos.authorizer import AuthorizerDto
from api.modules.merchants.v1.enums.category_codes import CategoryCodes
from api.modules.transactions.v1.enums.transaction_code import TransactionCode


class TransactionService:
    def __init__(self, account_service: AccountService = Depends(), merchant_service: MerchantService = Depends()) -> None:
        self.account_service = account_service
        self.merchant_service = merchant_service

    async def authorize(self, data: AuthorizerDto.Data, *, fallback: bool = False) -> TransactionCode:
        account = await self.account_service.read_one(AccountDto.ReadOne.Parameters(id=data.account_id))

        if data.category_code not in CategoryCodes.list() and (
            merchant := await self.merchant_service.read_one(MerchantDto.ReadOne.Parameters(name=data.merchant))
        ):
            data.category_code = merchant.category_code

        category = next((
            category_code.name for category_code in CategoryCodes
                if data.category_code in category_code.value
            ), None
        )

        balance = None

        categories = filter(
            None, [category] + (["cash"] if fallback else [])
        )

        for category in categories:
            if (balance := getattr(account.balance, category) - data.price) >= 0:
                break

        if balance is not None and balance >= 0:
            account_balance = {
                **account.balance.model_dump(), category: balance
            }

            await self.account_service.update(
                AccountDto.ReadOne.Parameters(id=account.id), AccountDto.Update.Data(balance=account_balance)
            )

            return TransactionCode.authorized

        return TransactionCode.unauthorized
