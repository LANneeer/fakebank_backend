from uuid import uuid4

from django.db import models
from django.db.models.functions import Now
from djmoney.models.fields import MoneyField

from bank.mixins import TimestampMixin
from payments.choices import Status


class Invoice(TimestampMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='KZT'
    )
    redirect_url = models.URLField(
        max_length=1023,
    )
    callback_url = models.URLField(
        max_length=1023,
    )
    payment_url = models.URLField(
        max_length=1023,
    )
    callback_data = models.CharField(
        max_length=1023,
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    expiration_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expiration_date__gte=Now()),
                name='expiration_date_cannot_be_past_date'
            )
        ]
