from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from loan.models import Bank, LoanType, BankLoanType, Loan

class LoanAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.bank = Bank.objects.create(name='Test Bank', code='TST')
        self.loan_type = LoanType.objects.create(
            name='Personal Loan',
            payment_frequency='MONTHLY',
            min_amount=10000,
            max_amount=1000000,
            min_term=6,
            max_term=60
        )
        self.bank_loan_type = BankLoanType.objects.create(
            bank=self.bank,
            loan_type=self.loan_type,
            interest_rate=10.5,
            processing_fee_percentage=1.5
        )
        
        self.loan_data = {
            'bank_loan_type': self.bank_loan_type.id,
            'amount': '50000.00',
            'term_months': 12,
            'compound_period': 'MONTHLY_APR'
        }
        self.loan = Loan.objects.create(**self.loan_data)

    def test_create_loan(self):
        url = reverse('loan:loan-list')
        response = self.client.post(url, self.loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)
        self.assertIn('monthly_payment', response.data)

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

    def test_update_loan(self):
        url = reverse('loan:loan-detail', kwargs={'pk': self.loan.pk})
        updated_data = {
            'bank_loan_type': self.bank_loan_type.id,
            'amount': '60000.00',
            'term_months': 24,
            'compound_period': 'MONTHLY_APR'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan.refresh_from_db()
        self.assertEqual(str(self.loan.amount), '60000.00')

    def test_delete_loan(self):
        url = reverse('loan:loan-detail', kwargs={'pk': self.loan.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Loan.objects.count(), 0)

    def test_calculate_loan(self):
        url = reverse('loan:bankloantype-calculate')
        data = {
            'bank_loan_type_id': self.bank_loan_type.id,
            'amount': '50000.00',
            'term_months': 12,
            'compound_period': 'MONTHLY_APR'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment_amount', response.data)
        self.assertIn('total_payment', response.data)
        self.assertIn('total_interest', response.data)
        self.assertIn('processing_fee', response.data)
        self.assertIn('schedule', response.data)

    def test_loan_statistics(self):
        url = reverse('loan:loan-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_loans', response.data)
        self.assertIn('avg_amount', response.data)
        self.assertIn('avg_interest_rate', response.data)
        self.assertIn('avg_term_months', response.data)

    def test_filter_loans(self):
        url = reverse('loan:loan-list')
        response = self.client.get(url, {'min_amount': '40000', 'max_amount': '60000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get(url, {'min_amount': '60000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_order_loans(self):
        Loan.objects.create(
            bank_loan_type=self.bank_loan_type,
            amount='30000.00',
            term_months=24,
            compound_period='MONTHLY_APR'
        )
        url = reverse('loan:loan-list')
        response = self.client.get(url, {'ordering': 'amount'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['amount'], '30000.00')

        response = self.client.get(url, {'ordering': '-amount'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['amount'], '50000.00')

