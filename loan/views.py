from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Loan, AmortizationSchedule
from .serializers import LoanSerializer
from .utils import calculate_loan_amortization

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan = serializer.save()
        
        # Calculate amortization schedule
        calculations = calculate_loan_amortization(loan)
        
        # Save amortization schedule
        schedule_objects = []
        for entry in calculations['schedule']:
            entry['loan'] = loan
            schedule_objects.append(AmortizationSchedule(**entry))
        AmortizationSchedule.objects.bulk_create(schedule_objects)
        
        # Update loan with calculated totals
        loan.monthly_payment = calculations['monthly_payment']
        loan.total_payment = calculations['total_payment']
        loan.total_interest = calculations['total_interest']
        loan.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate loan details without saving"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan = Loan(**serializer.validated_data)
        calculations = calculate_loan_amortization(loan)
        return Response(calculations)