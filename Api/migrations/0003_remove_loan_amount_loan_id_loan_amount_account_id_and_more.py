# Generated by Django 4.2.2 on 2023-06-19 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_alter_loan_amount_manager_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan_amount',
            name='loan_id',
        ),
        migrations.AddField(
            model_name='loan_amount',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.account'),
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
