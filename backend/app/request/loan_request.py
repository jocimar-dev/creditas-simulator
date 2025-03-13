from datetime import date

from pydantic import BaseModel

from backend.app.models.contact_model import ContactRequest
from backend.app.models.financial_model import FinancialRequest
from backend.app.models.personal_model import PersonalRequest
from backend.app.models.principal_model import PrincipalDataRequest


class LoanSimulationRequest(BaseModel):
    principal_data: PrincipalDataRequest
    personal_request: PersonalRequest
    contact_request: ContactRequest
    financial_request: FinancialRequest
