from enum import Enum


class TransactionCode(str, Enum):
    authorized = "00"
    unauthorized = "51"
    failure = "07"
