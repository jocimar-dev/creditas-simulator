import logging
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_interest_rate(birth_date: date) -> float:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    logger.info("Calculating interest rate for age: %s", age)

    interest_rates = {
        range(0, 26): 0.05,
        range(26, 41): 0.03,
        range(41, 61): 0.02
    }

    for age_range, rate in interest_rates.items():
        if age in age_range:
            logger.info("Interest rate found: %s", rate)
            return rate

    logger.info("Default interest rate applied: 0.04")
    return 0.04

def calculate_loan(loan_amount: float, interest_rate: float, months: int):
    logger.info("Calculating loan: loan_amount=%s, interest_rate=%s, months=%s", loan_amount, interest_rate, months)
    monthly_rate = interest_rate / 12
    if monthly_rate == 0:
        monthly_payment = loan_amount / months
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / (
                    (1 + monthly_rate) ** months - 1)

    total_payment = monthly_payment * months
    total_interest = total_payment - loan_amount

    result = {
        "monthly_payment": round(monthly_payment, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }

    logger.info("Loan calculation result: %s", result)
    return result