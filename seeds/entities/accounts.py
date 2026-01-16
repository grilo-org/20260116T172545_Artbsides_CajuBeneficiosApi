from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession

from api.modules.accounts.v1.entities.account import Account
from api.modules.accounts.v1.entities.account_balance import AccountBalance


async def accounts(db_session: AsyncIOMotorClientSession) -> list[PydanticObjectId]:
    accounts = [
        Account(
            id="6712b3eb3ec7354864d4274f",
            balance=AccountBalance(food=12, meal=12, cash=12)
        ),
        Account(
            id="6712b3eb3ec7354864d42750",
            balance=AccountBalance(food=24, meal=24, cash=24)
        )
    ]

    return (
        await Account.insert_many(
            accounts, session=db_session
        )
    ).inserted_ids
