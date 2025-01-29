from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, LoanStatisticsView

app_name = 'loan'

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', LoanStatisticsView.as_view(), name='loan-statistics'),
]