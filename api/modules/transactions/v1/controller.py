from fastapi import Depends

from api.routers.router import router
from api.modules.transactions.v1.service import TransactionService
from api.modules.transactions.v1.dtos.authorizer import AuthorizerDto


@router.post("/v1/transactions/authorizer",
    tags=["Transactions"], response_model_by_alias=False
)
async def authorizer(
    data: AuthorizerDto.Data,
    parameters: AuthorizerDto.Parameters = Depends(),
    transaction_service: TransactionService = Depends()
) -> AuthorizerDto.Response:
    return await transaction_service.authorize(data, fallback=parameters.fallback)
