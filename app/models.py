from pydantic import BaseModel
from datetime import date

class LoanSimulationRequest(BaseModel):
    loan_amount: float
    birth_date: date
    months: int
