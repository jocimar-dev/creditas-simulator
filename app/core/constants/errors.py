# backend/app/constants/errors.py

LOAN_AMOUNT_OUT_OF_RANGE = "Loan amount must be between 2000 and 50000."
GUARANTEE_REQUIRED = "Real estate value and/or vehicle value must be provided."
GUARANTEE_INSUFFICIENT = "Guarantee value must be at least 50% of the loan amount."
EXPENSES_EXCEED_LIMIT = "Monthly expenses exceed 70% of monthly income."
INCOME_PER_DEPENDENT_TOO_LOW = "Monthly income per dependent is less than 700."
INSTALLMENT_LIMIT_LOW = "Loan amount up to 2000 can only be paid in up to 12 installments."
INSTALLMENT_LIMIT_MEDIUM = "Loan amount up to 5000 can only be paid in up to 24 installments."
INSTALLMENT_LIMIT_HIGH = "Loan amount up to 15000 can only be paid in up to 36 installments."
INSTALLMENT_LIMIT_MAX = "Loan amount above 15000 can only be paid in up to 48 installments."
MONTHLY_PAYMENT_EXCEEDS_LIMIT = "Monthly payment exceeds 30% of monthly income."
