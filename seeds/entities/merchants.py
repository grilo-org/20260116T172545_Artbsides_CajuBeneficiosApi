from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession

from api.modules.merchants.v1.entities.merchant import Merchant
from api.modules.merchants.v1.enums.category_codes import CategoryCodes


async def merchants(db_session: AsyncIOMotorClientSession) -> list[PydanticObjectId]:
    category_codes = CategoryCodes.list()

    merchants = [
        Merchant(
            id="6713f083d497bf77f0924620",
            name="UBER TRIP                   SAO PAULO BR",
            category_code=category_codes[0]
        ),
        Merchant(
            id="6713f08ae6b1592ed5d4969f",
            name="UBER EATS                   SAO PAULO BR",
            category_code=category_codes[1]
        ),
        Merchant(
            id="6713f0907931e267e01a8299",
            name="PAG*JoseDaSilva          RIO DE JANEI BR",
            category_code=category_codes[2]
        ),
        Merchant(
            id="6713f093b8f5b8953ee9383f",
            name="PICPAY*BILHETEUNICO           GOIANIA BR",
            category_code=category_codes[3]
        )
    ]

    return (
        await Merchant.insert_many(
            merchants, session=db_session
        )
    ).inserted_ids
