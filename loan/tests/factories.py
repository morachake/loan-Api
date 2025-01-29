import factory
from factory.django import DjangoModelFactory
from ..models import Loan

class LoanFactory(DjangoModelFactory):
    class Meta:
        model = Loan

    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, min_value=1000, max_value=1000000)
    term_years = factory.Faker('random_int', min=1, max=30)
    term_months = factory.Faker('random_int', min=0, max=11)
    interest_rate = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=0.01, max_value=30)
    compound_period = 'MONTHLY_APR'
    payment_frequency = 'MONTHLY'