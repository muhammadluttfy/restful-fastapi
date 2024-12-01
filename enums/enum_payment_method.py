from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "CASH"
    NON_CASH = "NON_CASH"