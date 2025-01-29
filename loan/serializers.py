from rest_framework import serializers
from .models import Loan, AmortizationSchedule

class AmortizationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmortizationSchedule
        fields = ['payment_number', 'beginning_balance', 'payment', 
                 'principal', 'interest', 'ending_balance']

class LoanSerializer(serializers.ModelSerializer):
    schedule = AmortizationScheduleSerializer(many=True, read_only=True)
    total_payment = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_interest = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    monthly_payment = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'amount', 'term_years', 'term_months', 'interest_rate',
                 'compound_period', 'payment_frequency', 'monthly_payment',
                 'total_payment', 'total_interest', 'schedule']