from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Bank
from .serializers import BankSerializer, LoanCalculationRequestSerializer, LoanCalculationResponseSerializer
from .services import calculate_loan_amortization

class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class LoanCalculatorView(views.APIView):
    def post(self, request):
        serializer = LoanCalculationRequestSerializer(data=request.data)
        if serializer.is_valid():
            loan_data = serializer.validated_data
            
            # If interest_rate is not provided, try to get it from the bank
            if 'interest_rate' not in loan_data:
                try:
                    bank = Bank.objects.get(name=loan_data['bank'])
                    loan_data['interest_rate'] = bank.interest_rate
                except Bank.DoesNotExist:
                    return Response({"error": "Bank not found and interest rate not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            calculation_result = calculate_loan_amortization(loan_data)
            response_serializer = LoanCalculationResponseSerializer(calculation_result)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

