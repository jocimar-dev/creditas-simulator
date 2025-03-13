from backend.app.mapper.response_mapper import map_to_loan_simulation_response
from backend.app.request.loan_request import LoanSimulationRequest
from backend.app.response.loan_result import LoanSimulationResponse
from backend.app.service.services import get_interest_rate, calculate_loan, convert_currency


def create_loan_simulation_response(request: LoanSimulationRequest) -> LoanSimulationResponse:
    if request.principal_data.loan_amount <= 0 or request.principal_data.installment <= 0:
        raise ValueError("Loan amount and installment must be greater than zero.")

    interest_rate = get_interest_rate(request.principal_data.birth_date, request.principal_data.interest_rate_type)
    loan_amount_converted = convert_currency(request.principal_data.loan_amount, request.principal_data.currency, "BRL")
    simulation_result = calculate_loan(loan_amount_converted, interest_rate, request.principal_data.installment, request.principal_data.currency)

    return map_to_loan_simulation_response(request, simulation_result)