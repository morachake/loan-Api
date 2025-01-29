# Generated by Django 4.2.18 on 2025-01-29 22:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_bank_bankloantype_loantype_alter_loan_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bankloantype',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='loan',
            name='payment_frequency',
            field=models.CharField(choices=[('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('QUARTERLY', 'Quarterly'), ('ANNUALLY', 'Annually')], default='MONTHLY', max_length=20),
        ),
        migrations.AddField(
            model_name='loan',
            name='term_years',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='bankloantype',
            name='bank',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankloantype',
            name='loan_type',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankloantype',
            name='processing_fee_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='loan',
            name='term_months',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(11)]),
        ),
    ]
