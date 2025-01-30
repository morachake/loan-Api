from decimal import Decimal, ROUND_HALF_UP
from .exceptions import LoanCalculationError

def calculate_loan_amortization(loan_data):
    try:
        principal = Decimal(str(loan_data['loan_amount']))
        annual_rate = Decimal(str(loan_data['interest_rate'])) / Decimal('100')
        term_years = Decimal(str(loan_data['loan_term_years']))
        term_months = Decimal(str(loan_data['loan_term_months']))
        compound_period = loan_data['compound_period']
        payment_frequency = loan_data['payment_frequency']

        # Calculate total term in months
        total_term_months = term_years * Decimal('12') + term_months

        # Define compounds per year and payments per year
        compounds_per_year = {
            'ANNUALLY': 1,
            'SEMI_ANNUALLY': 2,
            'QUARTERLY': 4,
            'MONTHLY_APR': 12,
            'SEMI_MONTHLY': 24,
            'BIWEEKLY': 26,
            'WEEKLY': 52,
            'DAILY': 365,
            'CONTINUOUS': float('inf')
        }

        payments_per_year = {
            'EVERYDAY': 365,
            'EVERY_WEEK': 52,
            'EVERY_WEEKS': 26,
            'EVERY_HALF_MONTH': 24,
            'EVERY_MONTH': 12,
            'EVERY_6_MONTHS': 2,
            'ANNUALLY': 1
        }

        # Get number of compounds and payments per year
        compounds = compounds_per_year[compound_period]
        payments = payments_per_year[payment_frequency]

        # Calculate total number of payments
        total_payments = (total_term_months * Decimal(str(payments)) / Decimal('12')).to_integral_value(rounding=ROUND_HALF_UP)

        # Calculate effective interest rate per payment period
        if compound_period == 'CONTINUOUS':
            effective_rate = (Decimal.exp(annual_rate) - 1) / Decimal(str(payments))
        else:
            effective_rate = ((1 + annual_rate / Decimal(str(compounds))) ** Decimal(str(compounds)) - 1) / Decimal(str(payments))

        # Calculate payment amount
        if effective_rate == Decimal('0'):
            payment_amount = principal / total_payments
        else:
            payment_amount = (principal * effective_rate * (1 + effective_rate) ** total_payments) / ((1 + effective_rate) ** total_payments - 1)

        # Round payment amount to 2 decimal places
        payment_amount = payment_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Generate amortization schedule
        schedule = []
        balance = principal
        total_interest = Decimal('0.00')

        for payment_number in range(1, int(total_payments) + 1):
            interest_amount = (balance * effective_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            principal_amount = (payment_amount - interest_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Adjust last payment to account for rounding
            if payment_number == int(total_payments):
                principal_amount = balance
                payment_amount = principal_amount + interest_amount

            beginning_balance = balance
            balance = (balance - principal_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_interest += interest_amount

            schedule.append({
                'payment_number': payment_number,
                'beginning_balance': beginning_balance,
                'payment_amount': payment_amount,
                'principal_amount': principal_amount,
                'interest_amount': interest_amount,
                'ending_balance': balance
            })

        return {
            'payment_amount': payment_amount,
            'total_payments': int(total_payments),
            'total_interest': total_interest,
            'amortization_schedule': schedule
        }

    except Exception as e:
        raise LoanCalculationError(f"Error calculating loan details: {str(e)}")

