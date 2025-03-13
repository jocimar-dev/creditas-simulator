import logging

from app.dtos.loan_result import LoanSimulationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def map_to_loan_simulation_response(request, simulation_result) -> LoanSimulationResponse:
    responses = LoanSimulationResponse(
        full_name=request.personal_request.full_name,
        document_number_partial=request.personal_request.document_number[-4:],
        total_payment=round(simulation_result["total_payment"], 2),
        monthly_payment=round(simulation_result["monthly_payment"], 2),
        total_interest=round(simulation_result["total_interest"], 2),
        monthly_rate=round(simulation_result["monthly_rate"], 4),
        annual_rate=round(simulation_result["annual_rate"], 2),
        installment=request.principal_data.installment,
        guarantee_value=round((request.financial_request.real_estate_value or 0) + (request.financial_request.vehicle_value or 0), 2)
    )
    logger.info("Response: %s", responses)
    return responses