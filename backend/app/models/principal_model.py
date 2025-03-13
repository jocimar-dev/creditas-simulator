from datetime import date
from pydantic import BaseModel
from typing import Literal

class PrincipalDataRequest(BaseModel):
    loan_amount: float
    birth_date: date
    installment: int
    interest_rate_type: Literal["fixed", "variable"]
    currency: Literal["USD", "EUR", "BRL"]