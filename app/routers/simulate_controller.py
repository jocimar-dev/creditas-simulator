import logging
from fastapi import APIRouter, Depends
from typing import List
import asyncio

from app.factories.email_factory import EmailFactory
from app.validators.auth.validate_token import validate_token
from app.validators.simulation.process_loan_simulation import process_loan_simulation
from app.dtos.loan_request import LoanSimulationRequest
from app.dtos.loan_result import LoanSimulationResponse
from app.service.messaging.email_service import EmailService

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
    logger.error("❌ SMTP environment variables are incomplete. Check your .env file.")
    raise ValueError("SMTP environment variables are incomplete.")

# Instanciando o EmailService com as variáveis carregadas corretamente
email_service = EmailService(
    smtp_server=smtp_server,
    smtp_port=int(smtp_port),
    username=smtp_username,
    password=smtp_password
)
email_factory = EmailFactory(email_service)

@router.post("/simulate", response_model=LoanSimulationResponse,
             summary="Simulate Loan", description=
             "Performs a simulation of an individual loan based on the data provided by the user.")
async def simulate_loan(request: LoanSimulationRequest):
    logger.info("Loan simulation request received for %s", request.personal_request.full_name)

    response = await process_loan_simulation(request)
    logger.info("Simulation response: %s", response)

    customer_name = request.personal_request.full_name.split()[0]
    email_factory.send_simulation_email(request.contact_request.email, customer_name, response)

    return response


@router.post("/simulate/batch", response_model=List[LoanSimulationResponse],
             summary="Simulate Loan Batch", description=
             "Runs multiple loan simulations in a single request, returning the results for each item in the list.")
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
