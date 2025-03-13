import pytest
from fastapi import HTTPException
from app import LoanSimulationRequest, PersonalRequest, ContactRequest, FinancialRequest, PrincipalDataRequest
from app import process_loan_simulation
from datetime import datetime

@pytest.mark.asyncio
async def test_process_loan_simulation_exceeds_income():
    request = LoanSimulationRequest(
        personal_request=PersonalRequest(
            full_name="John Doe",
            document_number="12345678900",
            marital_status="single",
            dependents=0
        ),
        contact_request=ContactRequest(
            address="Rua Exemplo, 123",
            phone="+55 11 91234-5678",
            email="john.doe@example.com"
        ),
        financial_request=FinancialRequest(
            monthly_income=1000,
            monthly_expenses=200,
            real_estate_value=50000,
            vehicle_value=20000
        ),
        principal_data=PrincipalDataRequest(
            loan_amount=20000,
            birth_date=datetime.strptime("1990-01-01", "%Y-%m-%d"),
            installment=2,
            interest_rate_type="fixed",
            currency="USD"
        )
    )

    with pytest.raises(HTTPException) as excinfo:
        await process_loan_simulation(request)
    assert excinfo.value.status_code == 400
    assert "Monthly payment exceeds 30% of monthly income." in str(excinfo.value.detail)
