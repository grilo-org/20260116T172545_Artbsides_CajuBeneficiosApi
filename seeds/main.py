import asyncio

from seeds.entities.accounts import accounts
from seeds.entities.merchants import merchants

from api.confs.database import mongodb_session
from api.confs.settings import settings
from api.modules.accounts.v1.entities.account import Account
from api.modules.merchants.v1.entities.merchant import Merchant


async def populate_database() -> None:
    db_session = await mongodb_session(document_models = [
        Account, Merchant
    ])

    async with db_session.start_transaction():
        await accounts(db_session)
        await merchants(db_session)

async def drop_database() -> None:
    if settings.APP_ENVIRONMENT == "tests":
        (await mongodb_session()).client.drop_database(settings.DATABASE_NAME)


if __name__ == "__main__":
    asyncio.run(populate_database())
