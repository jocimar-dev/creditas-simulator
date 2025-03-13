from fastapi import HTTPException

from app.dtos.loan_request import LoanSimulationRequest
from app.core.constants import errors


def validate_loan_request(request: LoanSimulationRequest):
    _validate_loan_amount_range(request)
    _validate_guarantee_presence(request)
    _validate_guarantee_value(request)
    _validate_expenses_vs_income(request)
    _validate_income_per_dependent(request)
    _validate_installment_limit(request)


def _validate_loan_amount_range(request: LoanSimulationRequest):
    if request.principal_data.loan_amount < 2000 or request.principal_data.loan_amount > 50000:
        raise HTTPException(status_code=400, detail=errors.LOAN_AMOUNT_OUT_OF_RANGE)


def _validate_guarantee_presence(request: LoanSimulationRequest):
    if request.financial_request.real_estate_value is None and request.financial_request.vehicle_value is None:
        raise HTTPException(status_code=400, detail=errors.GUARANTEE_REQUIRED)


def _validate_guarantee_value(request: LoanSimulationRequest):
    guarantee_value = (request.financial_request.real_estate_value or 0) + (request.financial_request.vehicle_value or 0)
    if guarantee_value < 0.5 * request.principal_data.loan_amount:
        raise HTTPException(status_code=400, detail=errors.GUARANTEE_INSUFFICIENT)


def _validate_expenses_vs_income(request: LoanSimulationRequest):
    if request.financial_request.monthly_expenses > 0.7 * request.financial_request.monthly_income:
        raise HTTPException(status_code=400, detail=errors.EXPENSES_EXCEED_LIMIT)


def _validate_income_per_dependent(request: LoanSimulationRequest):
    dependents_factor = request.personal_request.dependents + 1
    if request.financial_request.monthly_income / dependents_factor < 700:
        raise HTTPException(status_code=400, detail=errors.INCOME_PER_DEPENDENT_TOO_LOW)


def _validate_installment_limit(request: LoanSimulationRequest):
    amount = request.principal_data.loan_amount
    installments = request.principal_data.installment

    if amount <= 2000 and installments > 12:
        raise HTTPException(status_code=400, detail=errors.INSTALLMENT_LIMIT_LOW)
    elif amount <= 5000 and installments > 24:
        raise HTTPException(status_code=400, detail=errors.INSTALLMENT_LIMIT_MEDIUM)
    elif amount <= 15000 and installments > 36:
        raise HTTPException(status_code=400, detail=errors.INSTALLMENT_LIMIT_HIGH)
    elif amount > 15000 and installments > 48:
        raise HTTPException(status_code=400, detail=errors.INSTALLMENT_LIMIT_MAX)
