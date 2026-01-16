from fastapi import Depends, APIRouter

from api.confs.settings import settings
from api.utils.authorization import Authorization


router = APIRouter(
    prefix=settings.APP_PREFIX, dependencies=[
        Depends(Authorization())
    ]
)
