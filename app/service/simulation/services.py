import logging
import os
from datetime import date

from forex_python.converter import CurrencyRates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_interest_rate(birth_date: date) -> float:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    logger.info("Calculating interest rate for age: %s years", age)
    if age <= 25:
        return 0.05
    elif 26 <= age <= 40:
        return 0.03
    elif 41 <= age <= 60:
        return 0.02
    else:
        return 0.04

def calculate_loan(loan_amount: float, interest_rate: float, installment: int):
    total_interest = loan_amount * interest_rate
    total_payment = loan_amount + total_interest
    monthly_payment = total_payment / installment
    monthly_rate = interest_rate / 12
    annual_rate = interest_rate
    return {
        "total_payment": total_payment,
        "monthly_payment": monthly_payment,
        "total_interest": total_interest,
        "monthly_rate": monthly_rate,
        "annual_rate": annual_rate
    }


def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount

    if os.getenv("USE_SIMULATED_CONVERSION", "false").lower() == "true":
        conversion_rates = {
            ("USD", "BRL"): 5.0,
            ("EUR", "BRL"): 6.0,
            ("BRL", "USD"): 0.2,
            ("BRL", "BRL"): 1.0
        }
        return amount * conversion_rates[(from_currency, to_currency)]
    try:
        c = CurrencyRates()
        return c.convert(from_currency, to_currency, amount)
    except Exception as e:
        logging.warning(f"Erro ao converter moeda: {e}. Retornando valor original.")
        return amount
