from decimal import Decimal, ROUND_HALF_UP
from .exceptions import LoanCalculationError

def calculate_loan_amortization(loan_data):
    try:
        principal = Decimal(str(loan_data['loan_amount']))
        annual_rate = Decimal(str(loan_data['interest_rate'])) / Decimal('100')
        term_years = Decimal(str(loan_data['loan_term_years']))
        term_months = Decimal(str(loan_data['loan_term_months']))
        payment_frequency = loan_data['payment_frequency']

        # Calculate total term in months
        total_term_months = term_years * Decimal('12') + term_months

        # Get number of payments per year
        payments_per_year = {
            'MONTHLY': Decimal('12'),
            'DAILY': Decimal('365'),
            'WEEKLY': Decimal('52'),
            'ANNUALLY': Decimal('1')
        }[payment_frequency]

        # Calculate total number of payments
        total_payments = (total_term_months * payments_per_year / Decimal('12')).to_integral_value(rounding=ROUND_HALF_UP)

        # Calculate effective interest rate per payment period
        r = (Decimal('1') + annual_rate/Decimal('12')) ** (Decimal('12')/payments_per_year) - Decimal('1')

        # Calculate payment amount
        if r == Decimal('0'):
            payment_amount = principal / total_payments
        else:
            payment_amount = (principal * r * (Decimal('1') + r) ** total_payments) / ((Decimal('1') + r) ** total_payments - Decimal('1'))

        # Round payment amount to 2 decimal places
        payment_amount = payment_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Generate amortization schedule
        schedule = []
        balance = principal
        total_interest = Decimal('0.00')

        for payment_number in range(1, int(total_payments) + 1):
            interest_amount = (balance * r).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
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
            'monthly_payment': payment_amount,
            'total_payments': int(total_payments),
            'total_interest': total_interest,
            'amortization_schedule': schedule
        }

    except Exception as e:
        raise LoanCalculationError(f"Error calculating loan details: {str(e)}")

