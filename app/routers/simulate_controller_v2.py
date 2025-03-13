import logging
from fastapi import APIRouter, Depends
from typing import List
import asyncio
import os
from dotenv import load_dotenv

from app.routers.simulate_controller import email_service
from app.dtos.loan_request import LoanSimulationRequest
from app.dtos.loan_result import LoanSimulationResponse
from app.adapters.messaging.generate_email_body import generate_email_body
from app.validators.auth.validate_token import validate_token
from app.validators.simulation.process_loan_simulation import process_loan_simulation
from app.service.messaging.sqs_service import SQSService

router = APIRouter()
load_dotenv()
logger = logging.getLogger(__name__)

# simulate_controller_v2.py

sqs_service = SQSService(queue_name="loan-simulation-queue", use_localstack=True)

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", 587))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
queue_name = os.getenv("SQS_QUEUE_NAME")
region = os.getenv("AWS_REGION")


@router.post("/v2/simulate/batch", response_model=List[LoanSimulationResponse],
                dependencies=[Depends(validate_token)],
                summary="Simulate Loan Batch - Version 2.0", description=
             "Version 2 of the individual loan simulation endpoint with performance improvements and asynchronous validation."
             )
async def simulate_loan_batch(
    requests: List[LoanSimulationRequest]
):
    logger.info("Batch loan simulation request received: %d requests", len(requests))

    async def process_request(request: LoanSimulationRequest):
        response = await process_loan_simulation(request)
        customer_name = request.personal_request.full_name.split()[0]
        email_body = generate_email_body(customer_name, response.model_dump_json(indent=2))

        # Envia email em background (caso método seja async)
        asyncio.create_task(
            email_service.send_email(
                to_email=str(request.contact_request.email),
                subject="Loan Simulation Results",
                body=email_body
            )
        )

        # Envia mensagem ao SQS em background (certo agora)
        asyncio.create_task(
            sqs_service.send_message(response.model_dump())
        )

        return response

    tasks = [process_request(request) for request in requests]
    responses = await asyncio.gather(*tasks)

    logger.info("Batch simulation responses generated")
    return responses
