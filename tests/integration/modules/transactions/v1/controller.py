import jwt
import pytest

from faker import Faker
from typing import AsyncGenerator
from asyncio import sleep
from fastapi import status
from datetime import datetime, timezone, timedelta
from seeds.main import drop_database, populate_database
from fastapi.testclient import TestClient

from api.main import app
from api.confs.settings import settings
from api.modules.merchants.v1.enums.category_codes import CategoryCodes
from api.modules.transactions.v1.enums.transaction_code import TransactionCode


class TestTransactionsController:
    client = TestClient(app)
    category_codes = CategoryCodes.list()
    authorization: dict
    payload: dict

    @pytest.fixture(autouse=True, scope="class")
    async def setup_class(self) -> AsyncGenerator[None, None]:
        await drop_database()

        await sleep(5)
        await populate_database()

        yield

        await drop_database()


    @pytest.fixture(autouse=True)
    def setup_function(self, faker: Faker) -> None:
        self.authorization = {
            "Authorization": f"Bearer {
                jwt.encode(
                    key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM, payload={
                        "exp": (datetime.now(timezone.utc) + timedelta(seconds=5)).timestamp()
                    }
                )
            }"
        }

        self.payload = {
            "account": "6712b3eb3ec7354864d4274f",
            "totalAmount": faker.pyfloat(right_digits=2, min_value=0, max_value=4),
            "mcc": str(faker.random_number(digits=4)),
            "merchant": "UBER TRIP                   SAO PAULO BR"
        }

    def authorizer_forbidden_test(self) -> None:
        response = self.client.post("/v1/transactions/authorizer")

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.failure

    def authorizer_account_not_found_test(self) -> None:
        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={**self.payload, "account": "671666852ae566a15b7e4e18"}
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.failure

    def authorizer_food_category_test(self) -> None:
        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={**self.payload, "mcc": self.category_codes[0]}
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized

        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={**self.payload, "mcc": self.category_codes[1]}
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized

    def authorizer_meal_category_test(self) -> None:
        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={**self.payload, "mcc": self.category_codes[2]}
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized

        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={**self.payload, "mcc": self.category_codes[3]}
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized

    def authorizer_merchant_category_test(self) -> None:
        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json=self.payload
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized

    def authorizer_unsuficient_money_test(self, faker: Faker) -> None:
        response = self.client.post("/v1/transactions/authorizer",
            headers=self.authorization, json={
                **self.payload, "totalAmount": faker.pyfloat(right_digits=2, min_value=8)
            }
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.unauthorized

    def authorizer_cash_category_test(self, faker: Faker) -> None:
        response = self.client.post("/v1/transactions/authorizer?fallback=true",
            headers=self.authorization, json={
                **self.payload, "totalAmount": faker.pyfloat(right_digits=2, max_value=12)
            }
        )

        assert response.content is not None
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["code"] == TransactionCode.authorized
