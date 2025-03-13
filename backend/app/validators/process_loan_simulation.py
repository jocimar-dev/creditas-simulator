from fastapi import HTTPException

from backend.app.mapper.response_mapper import map_to_loan_simulation_response
from backend.app.request.loan_request import LoanSimulationRequest
from backend.app.response.loan_result import LoanSimulationResponse
from backend.app.service.services import get_interest_rate, convert_currency, calculate_loan
from backend.app.validators.validate_loan_request import validate_loan_request


async def process_loan_simulation(request: LoanSimulationRequest) -> LoanSimulationResponse:
    validate_loan_request(request)

    interest_rate = get_interest_rate(request.principal_data.birth_date)
    loan_amount_converted = convert_currency(request.principal_data.loan_amount, request.principal_data.currency, "USD")
    simulation_result = calculate_loan(loan_amount_converted, interest_rate, request.principal_data.installment)

    if simulation_result["monthly_payment"] > 0.3 * request.financial_request.monthly_income:
        raise HTTPException(status_code=400, detail="Monthly payment exceeds 30% of monthly income.")

    return map_to_loan_simulation_response(request, simulation_result)