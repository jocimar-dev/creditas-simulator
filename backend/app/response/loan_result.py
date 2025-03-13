from typing import Optional

from pydantic import BaseModel

# backend/app/response/loan_result.py
from pydantic import BaseModel

class LoanSimulationResponse(BaseModel):
    full_name: str
    document_number_partial: str
    total_payment: float
    monthly_payment: float
    total_interest: float
    monthly_rate: float
    annual_rate: float
    installment: int
    guarantee_value: float