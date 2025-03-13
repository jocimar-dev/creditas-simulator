from app.adapters.mapper.response_mapper import map_to_loan_simulation_response
from app.dtos.loan_request import LoanSimulationRequest
from app.dtos.loan_result import LoanSimulationResponse
from app.service.simulation.services import get_interest_rate, calculate_loan, convert_currency


def create_loan_simulation_response(request: LoanSimulationRequest) -> LoanSimulationResponse:
    if request.principal_data.loan_amount <= 0 or request.principal_data.installment <= 0:
        raise ValueError("Loan amount and installment must be greater than zero.")

    interest_rate = get_interest_rate(request.principal_data.birth_date)
    loan_amount_converted = convert_currency(request.principal_data.loan_amount, request.principal_data.currency, "BRL")
    simulation_result = calculate_loan(loan_amount_converted, interest_rate, request.principal_data.installment)

    return map_to_loan_simulation_response(request, simulation_result)