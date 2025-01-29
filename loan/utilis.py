from decimal import Decimal
import math

def calculate_loan_amortization(loan):
    """Calculate loan amortization schedule"""
    
    # Convert annual rate to monthly
    monthly_rate = float(loan.interest_rate) / 100 / 12
    
    # Calculate total number of payments
    total_months = (loan.term_years * 12) + loan.term_months
    
    # Calculate monthly payment using amortization formula
    amount = float(loan.amount)
    monthly_payment = amount * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
    
    schedule = []
    balance = amount
    total_interest = 0
    
    for payment_number in range(1, total_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        ending_balance = balance - principal_payment
        total_interest += interest_payment
        
        schedule.append({
            'payment_number': payment_number,
            'beginning_balance': Decimal(str(round(balance, 2))),
            'payment': Decimal(str(round(monthly_payment, 2))),
            'principal': Decimal(str(round(principal_payment, 2))),
            'interest': Decimal(str(round(interest_payment, 2))),
            'ending_balance': Decimal(str(round(ending_balance, 2)))
        })
        
        balance = ending_balance
    
    return {
        'monthly_payment': Decimal(str(round(monthly_payment, 2))),
        'total_payment': Decimal(str(round(monthly_payment * total_months, 2))),
        'total_interest': Decimal(str(round(total_interest, 2))),
        'schedule': schedule
    }