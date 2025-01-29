from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .factories import LoanFactory
from ..models import Loan

User = get_user_model()

class LoanViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.loan = LoanFactory()

    def test_create_loan(self):
        url = reverse('loan:loan-list')
        data = {
            'amount': '50000.00',
            'term_years': 1,
            'term_months': 0,
            'interest_rate': '10.00',
            'compound_period': 'MONTHLY_APR',
            'payment_frequency': 'MONTHLY'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)
        self.assertIsNotNone(response.data['monthly_payment'])

    def test_calculate_loan(self):
        url = reverse('loan:loan-calculate')
        data = {
            'amount': '50000.00',
            'term_years': 1,
            'term_months': 0,
            'interest_rate': '10.00',
            'compound_period': 'MONTHLY_APR',
            'payment_frequency': 'MONTHLY'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('monthly_payment', response.data)
        self.assertIn('total_payment', response.data)
        self.assertIn('total_interest', response.data)

    def test_get_loan_list(self):
        url = reverse('loan:loan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_loan_detail(self):
        url = reverse('loan:loan-detail', kwargs={'pk': self.loan.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.loan.pk)

    def test_loan_statistics(self):
        url = reverse('loan:loan-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_loans', response.data)
        self.assertIn('avg_amount', response.data)
        self.assertIn('avg_interest_rate', response.data)
        self.assertIn('avg_term_years', response.data)