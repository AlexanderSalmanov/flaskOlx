from helpers import AutoEnum
from enum import auto


class Status(AutoEnum):
    ACTIVE = auto()
    INACTIVE = auto()
    DELETED = auto()


class AdvertiserType(AutoEnum):
    PRIVATE = auto()
    COMPANY = auto()


class Currency(AutoEnum):
    UAH = auto()
    USD = auto()
    EUR = auto()
    PLN = auto()
