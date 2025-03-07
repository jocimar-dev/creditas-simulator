import logging
from fastapi import APIRouter, HTTPException
from app.models import LoanSimulationRequest
from app.services import get_interest_rate, calculate_loan

router = APIRouter()

# Basic logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/simulate")
def simulate_loan(request: LoanSimulationRequest):
    """
    Simulates a loan based on the provided data.

    Args:
        request (LoanSimulationRequest): Loan simulation request data, including
                                         loan amount, birthdate, and number of months.

    Returns:
        dict: Loan simulation result, including loan amount, number of months,
              interest rate, and detailed simulation results.

    Raises:
        HTTPException: If the loan amount or the number of months are less than or equal to zero.
    """
    logger.info("Loan simulation request received: %s", request)

    if request.loan_amount <= 0 or request.months <= 0:
        logger.error("Invalid loan amount or months: loan_amount=%s, months=%s", request.loan_amount, request.months)
        raise HTTPException(status_code=400, detail="Loan amount and months must be greater than zero.")

    interest_rate = get_interest_rate(request.birth_date)
    simulation_result = calculate_loan(request.loan_amount, interest_rate, request.months)

    response = {
        "loan_amount": request.loan_amount,
        "months": request.months,
        "interest_rate": round(interest_rate * 100, 2),
        "results": simulation_result
    }

    logger.info("Simulation response: %s", response)
    return response
