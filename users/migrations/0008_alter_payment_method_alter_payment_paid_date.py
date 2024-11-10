# Generated by Django 5.1.2 on 2024-11-10 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_payment_link_payment_session_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="method",
            field=models.CharField(
                blank=True,
                choices=[("transaction", "перевод"), ("cash", "наличные")],
                default="transaction",
                max_length=20,
                null=True,
                verbose_name="Метод платежа",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="paid_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                verbose_name="Дата оплаты",
            ),
        ),
    ]
