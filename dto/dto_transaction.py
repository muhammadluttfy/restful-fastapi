from typing import Optional
from pydantic import BaseModel
from enums.enum_payment_method import PaymentMethod
from enums.enum_payment_type import PaymentType


class InputTransaction(BaseModel):
    payment_type: PaymentType
    amount: int
    notes: Optional[str] = None
    method: PaymentMethod