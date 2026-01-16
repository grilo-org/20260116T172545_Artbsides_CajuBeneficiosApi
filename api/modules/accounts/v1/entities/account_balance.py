from beanie import DecimalAnnotation
from pydantic import BaseModel


class AccountBalance(BaseModel):
    food: DecimalAnnotation
    meal: DecimalAnnotation
    cash: DecimalAnnotation
