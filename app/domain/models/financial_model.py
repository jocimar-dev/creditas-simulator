from typing import Optional

from pydantic import BaseModel

class FinancialRequest(BaseModel):
    monthly_income: float
    monthly_expenses: float
    real_estate_value: Optional[float] = None
    vehicle_value: Optional[float] = None
