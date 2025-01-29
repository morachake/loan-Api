from decimal import Decimal

# Loan Amount Constraints
MIN_LOAN_AMOUNT = Decimal('1000.00')
MAX_LOAN_AMOUNT = Decimal('10000000.00')

# Interest Rate Constraints
MIN_INTEREST_RATE = Decimal('0.01')
MAX_INTEREST_RATE = Decimal('100.00')

# Term Constraints
MAX_TERM_YEARS = 30

# Payment Frequencies
PAYMENT_FREQUENCIES = {
    'WEEKLY': 'Weekly',
    'MONTHLY': 'Monthly',
    'QUARTERLY': 'Quarterly',
    'ANNUALLY': 'Annually',
}

# Compound Periods
COMPOUND_PERIODS = {
    'DAILY': 'Daily',
    'WEEKLY': 'Weekly',
    'MONTHLY_APR': 'Monthly (APR)',
    'QUARTERLY': 'Quarterly',
    'ANNUALLY': 'Annually',
}

# Frequency to number of payments per year mapping
PAYMENTS_PER_YEAR = {
    'WEEKLY': 52,
    'MONTHLY': 12,
    'QUARTERLY': 4,
    'ANNUALLY': 1,
}

# Compound frequency to number of compounds per year mapping
COMPOUNDS_PER_YEAR = {
    'DAILY': 365,
    'WEEKLY': 52,
    'MONTHLY_APR': 12,
    'QUARTERLY': 4,
    'ANNUALLY': 1,
}

