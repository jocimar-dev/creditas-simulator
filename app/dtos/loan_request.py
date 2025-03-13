from pydantic import BaseModel

from app.domain.models.contact_model import ContactRequest
from app.domain.models.financial_model import FinancialRequest
from app.domain.models.personal_model import PersonalRequest
from app.domain.models.principal_model import PrincipalDataRequest


class LoanSimulationRequest(BaseModel):
    principal_data: PrincipalDataRequest
    personal_request: PersonalRequest
    contact_request: ContactRequest
    financial_request: FinancialRequest
