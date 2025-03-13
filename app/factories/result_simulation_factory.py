from fastapi import HTTPException

from app.adapters.mapper.response_mapper import map_to_loan_simulation_response


async def checks_financial_capacity(request, simulation_result):
    if simulation_result.monthly_payment > 0.3 * request.financial_request.monthly_income:
        raise HTTPException(status_code=400, detail="Monthly payment exceeds 30% of monthly income.")
    response =map_to_loan_simulation_response(request, simulation_result)
    return response