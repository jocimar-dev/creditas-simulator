class LoanSimulationMapper:
    @staticmethod
    def map_guarantee(guarantee_request):
        if guarantee_request:
            real_estate_value = guarantee_request.real_estate_value
            vehicle_value = guarantee_request.vehicle_value
            if real_estate_value is not None:
                real_estate_value *= 0.9  # Depreciar 10%
            return {
                "real_estate_value": real_estate_value,
                "vehicle_value": vehicle_value,
            }
        return None

    @staticmethod
    def map_response(request, base_interest_rate, adjusted_interest_rate, simulation_result):
        return {
            "loan_amount": request.loan_amount,
            "interest_rate": {
                "base_rate": round(base_interest_rate * 100, 2),
                "adjusted_rate": round(adjusted_interest_rate * 100, 2),
            },
            "applicant": {
                "name": request.personal_request.full_name,
                "document_number": request.personal_request.document_number,
                "marital_status": request.personal_request.marital_status,
                "dependents": request.personal_request.dependents,
                "address": request.contact_request.address,
                "phone": request.contact_request.phone,
                "email": request.contact_request.email,
                "monthly_income": request.financial_request.monthly_income,
                "monthly_expenses": request.financial_request.monthly_expenses,
            },
            "guarantee": LoanSimulationMapper.map_guarantee(request.guarantee_request),
            "results": simulation_result,
            "installment": request.installment,
            "guarantee_value": (request.financial_request.real_estate_value or 0) + (request.financial_request.vehicle_value or 0)
        }
