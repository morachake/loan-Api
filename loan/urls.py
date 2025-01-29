from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankViewSet, LoanCalculatorView

router = DefaultRouter()
router.register(r'banks', BankViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate/', LoanCalculatorView.as_view(), name='loan-calculate'),
]

