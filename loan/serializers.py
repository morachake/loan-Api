from rest_framework import serializers
from .models import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name', 'interest_rate']

class LoanCalculationRequestSerializer(serializers.Serializer):
    bank = serializers.CharField(max_length=100)
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    loan_term_years = serializers.IntegerField(min_value=0)
    loan_term_months = serializers.IntegerField(min_value=0, max_value=11)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    compound_period = serializers.ChoiceField(choices=[('MONTHLY_APR', 'Monthly (APR)')])
    payment_frequency = serializers.ChoiceField(choices=[
        ('MONTHLY', 'Monthly'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('ANNUALLY', 'Annually')
    ])

class AmortizationEntrySerializer(serializers.Serializer):
    payment_number = serializers.IntegerField()
    beginning_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    principal_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    ending_balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class LoanCalculationResponseSerializer(serializers.Serializer):
    monthly_payment = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_payments = serializers.IntegerField()
    total_interest = serializers.DecimalField(max_digits=12, decimal_places=2)
    amortization_schedule = AmortizationEntrySerializer(many=True)

