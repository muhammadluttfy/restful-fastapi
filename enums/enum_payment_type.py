from enum import Enum

class PaymentType(str, Enum):
    INCOME = "INCOME"
    PURCHASE = "PURCHASE"
    INVEST = "INVEST"