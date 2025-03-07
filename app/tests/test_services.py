from app.services import get_interest_rate, calculate_loan
from datetime import date
import math

def test_get_interest_rate():
    assert math.isclose(get_interest_rate(date(2000, 1, 1)), 0.05, rel_tol=1e-9)
    assert math.isclose(get_interest_rate(date(1985, 1, 1)), 0.03, rel_tol=1e-9)
    assert math.isclose(get_interest_rate(date(1975, 1, 1)), 0.02, rel_tol=1e-9)
    assert math.isclose(get_interest_rate(date(1950, 1, 1)), 0.04, rel_tol=1e-9)


def test_calculate_loan():
    result = calculate_loan(10000, 0.03, 12)
    assert "monthly_payment" in result
    assert "total_payment" in result
    assert "total_interest" in result
    assert result["total_payment"] > 10000
