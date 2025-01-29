from django_filters import rest_framework as filters
from .models import Loan

class LoanFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    min_interest = filters.NumberFilter(field_name="bank_loan_type__interest_rate", lookup_expr='gte')
    max_interest = filters.NumberFilter(field_name="bank_loan_type__interest_rate", lookup_expr='lte')
    bank = filters.CharFilter(field_name="bank_loan_type__bank__code")
    loan_type = filters.CharFilter(field_name="bank_loan_type__loan_type__name")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Loan
        fields = ['bank_loan_type__bank', 'bank_loan_type__loan_type']

