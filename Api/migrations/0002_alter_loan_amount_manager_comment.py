# Generated by Django 4.2.2 on 2023-06-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_amount',
            name='manager_comment',
            field=models.TextField(default=''),
        ),
    ]
