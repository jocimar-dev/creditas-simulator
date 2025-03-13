from pydantic import EmailStr

from app.dtos.loan_result import LoanSimulationResponse
from app.adapters.messaging.generate_email_body import generate_email_body


class EmailFactory:
    def __init__(self, email_service):
        self.email_service = email_service

    def send_simulation_email(self, email: EmailStr, customer_name: str, response: LoanSimulationResponse):
        email_str = str(email)
        email_body = generate_email_body(customer_name, response.model_dump_json(indent=2))
        self.email_service.send_email(email_str, "Loan Simulation Results", email_body)
