# Generated by Django 4.2.18 on 2025-01-29 21:17

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amortizationschedule',
            options={'ordering': ['payment_number']},
        ),
        migrations.AlterModelOptions(
            name='loan',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='amortizationschedule',
            old_name='beginning_balance',
            new_name='balance',
        ),
        migrations.RenameField(
            model_name='amortizationschedule',
            old_name='ending_balance',
            new_name='interest_amount',
        ),
        migrations.RenameField(
            model_name='amortizationschedule',
            old_name='interest',
            new_name='payment_amount',
        ),
        migrations.RenameField(
            model_name='amortizationschedule',
            old_name='payment',
            new_name='principal_amount',
        ),
        migrations.RemoveField(
            model_name='amortizationschedule',
            name='principal',
        ),
        migrations.AddField(
            model_name='loan',
            name='monthly_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='total_interest',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='total_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('1000.00')), django.core.validators.MaxValueValidator(Decimal('1000000.00'))]),
        ),
        migrations.AlterField(
            model_name='loan',
            name='compound_period',
            field=models.CharField(choices=[('MONTHLY_APR', 'Monthly (APR)'), ('DAILY_APR', 'Daily (APR)'), ('SEMI_ANNUAL', 'Semi-Annual'), ('ANNUAL', 'Annual')], default='MONTHLY_APR', max_length=20),
        ),
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01')), django.core.validators.MaxValueValidator(Decimal('30.00'))]),
        ),
        migrations.AlterField(
            model_name='loan',
            name='payment_frequency',
            field=models.CharField(choices=[('MONTHLY', 'Every Month'), ('BI_WEEKLY', 'Every Two Weeks'), ('WEEKLY', 'Weekly')], default='MONTHLY', max_length=20),
        ),
        migrations.AlterField(
            model_name='loan',
            name='term_months',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(11)]),
        ),
        migrations.AlterField(
            model_name='loan',
            name='term_years',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['created_at'], name='loan_loan_created_ffcaf9_idx'),
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['amount'], name='loan_loan_amount_f37771_idx'),
        ),
    ]
