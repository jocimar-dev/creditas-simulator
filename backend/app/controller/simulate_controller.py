import logging
from fastapi import APIRouter
from typing import List
import asyncio

from backend.app.factory_backend.email_factory import EmailFactory
from backend.app.validators.process_loan_simulation import process_loan_simulation
from backend.app.request.loan_request import LoanSimulationRequest
from backend.app.response.loan_result import LoanSimulationResponse
from backend.app.service.email_service import EmailService

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
import os

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

logger.info(f"SMTP_SERVER: {smtp_server}")


# Validação básica para evitar valores None
if not all([smtp_server, smtp_port, smtp_username, smtp_password]):
    logger.error("❌ Variáveis de ambiente SMTP estão incompletas. Verifique seu arquivo .env.")
    raise ValueError("Variáveis de ambiente SMTP estão incompletas.")

# Instanciando o EmailService com as variáveis carregadas corretamente
email_service = EmailService(
    smtp_server=smtp_server,
    smtp_port=int(smtp_port),
    username=smtp_username,
    password=smtp_password
)
email_factory = EmailFactory(email_service)

@router.post("/simulate", response_model=LoanSimulationResponse)
async def simulate_loan(request: LoanSimulationRequest):
    logger.info("Loan simulation request received for %s", request.personal_request.full_name)

    response = await process_loan_simulation(request)
    logger.info("Simulation response: %s", response)

    customer_name = request.personal_request.full_name.split()[0]
    email_factory.send_simulation_email(request.contact_request.email, customer_name, response)

    return response


@router.post("/simulate/batch", response_model=List[LoanSimulationResponse])
async def simulate_loan_batch(requests: List[LoanSimulationRequest]):
    logger.info("Batch loan simulation request received: %d requests", len(requests))

    async def process_request(request: LoanSimulationRequest):
        response = await process_loan_simulation(request)

        # Send email with the simulation results
        customer_name = request.personal_request.full_name.split()[0]
        email_factory.send_simulation_email(request.contact_request.email, customer_name, response)

        return response

    tasks = [process_request(request) for request in requests]
    responses = await asyncio.gather(*tasks)
    logger.info("Batch simulation responses generated")
    return responses
