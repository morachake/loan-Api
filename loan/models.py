from django.db import models

class Loan(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_years = models.IntegerField()
    term_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    compound_period = models.CharField(
        max_length=20,
        choices=[
            ('MONTHLY_APR', 'Monthly (APR)'),
            ('DAILY_APR', 'Daily (APR)'),
        ],
        default='MONTHLY_APR'
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=[
            ('MONTHLY', 'Every Month'),
            ('BI_WEEKLY', 'Every Two Weeks'),
        ],
        default='MONTHLY'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class AmortizationSchedule(models.Model):
    loan = models.ForeignKey(Loan, related_name='schedule', on_delete=models.CASCADE)
    payment_number = models.IntegerField()
    beginning_balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    ending_balance = models.DecimalField(max_digits=10, decimal_places=2)