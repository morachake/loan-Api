from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        default=Decimal('5.00')  
    )

    def __str__(self):
        return f"{self.name} ({self.interest_rate}%)"

