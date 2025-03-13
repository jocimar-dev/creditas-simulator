from fastapi import HTTPException
from app.dtos.loan_request import LoanSimulationRequest

class LoanValidationService:
    @staticmethod
    def validate_loan_request(request: LoanSimulationRequest):
        service = LoanValidationService
        service._validate_loan_amount(request)
        service._validate_guarantee_value(request)
        service._validate_monthly_expenses(request)
        service._validate_monthly_income_per_dependent(request)
        service._validate_installment(request)

    @staticmethod
    def _validate_loan_amount(request: LoanSimulationRequest):
        if request.principal_data.loan_amount < 2000 or request.principal_data.loan_amount > 50000:
            raise HTTPException(status_code=400, detail="Loan amount must be between 2000 and 50000.")

    @staticmethod
    def _validate_guarantee_value(request: LoanSimulationRequest):
        if request.financial_request.real_estate_value is None and request.financial_request.vehicle_value is None:
            raise HTTPException(status_code=400, detail="Real estate value and/or vehicle value must be provided.")
        guarantee_value = (request.financial_request.real_estate_value or 0) + (request.financial_request.vehicle_value or 0)
        if guarantee_value < 0.5 * request.principal_data.loan_amount:
            raise HTTPException(status_code=400, detail="Guarantee value must be at least 50% of the loan amount.")

    @staticmethod
    def _validate_monthly_expenses(request: LoanSimulationRequest):
        if request.financial_request.monthly_expenses > 0.7 * request.financial_request.monthly_income:
            raise HTTPException(status_code=400, detail="Monthly expenses exceed 70% of monthly income.")

    @staticmethod
    def _validate_monthly_income_per_dependent(request: LoanSimulationRequest):
        dependents_factor = request.personal_request.dependents + 1
        if request.financial_request.monthly_income / dependents_factor < 700:
            raise HTTPException(status_code=400, detail="Monthly income per dependent is less than 700.")

    @staticmethod
    def _validate_installment(request: LoanSimulationRequest):
        if request.principal_data.loan_amount <= 2000 and request.principal_data.installment > 12:
            raise HTTPException(status_code=400, detail="Loan amount up to 2000 can only be paid in up to 12 installments.")
        elif request.principal_data.loan_amount <= 5000 and request.principal_data.installment > 24:
            raise HTTPException(status_code=400, detail="Loan amount up to 5000 can only be paid in up to 24 installments.")
        elif request.principal_data.loan_amount <= 15000 and request.principal_data.installment > 36:
            raise HTTPException(status_code=400, detail="Loan amount up to 15000 can only be paid in up to 36 installments.")
        elif request.principal_data.loan_amount > 15000 and request.principal_data.installment > 48:
            raise HTTPException(status_code=400, detail="Loan amount above 15000 can only be paid in up to 48 installments.")