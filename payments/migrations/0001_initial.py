# Generated by Django 4.2.2 on 2023-06-24 09:39

from django.db import migrations, models
import django.db.models.functions.datetime
import djmoney.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "amount_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("KZT", "Kazakhstani Tenge")],
                        default="KZT",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "amount",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2, default_currency="KZT", max_digits=10
                    ),
                ),
                ("redirect_url", models.URLField(max_length=1023)),
                ("callback_url", models.URLField(max_length=1023)),
                ("payment_url", models.URLField(max_length=1023)),
                ("callback_data", models.CharField(max_length=1023)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("canceled", "Canceled"),
                            ("paid", "Paid"),
                        ],
                        max_length=8,
                    ),
                ),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("expiration_date", models.DateTimeField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="invoice",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("expiration_date__gte", django.db.models.functions.datetime.Now())
                ),
                name="expiration_date_cannot_be_past_date",
            ),
        ),
    ]
