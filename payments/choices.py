from django.db import models


class Status(models.TextChoices):
    PENDING = 'pending'
    CANCELED = 'canceled'
    PAID = 'paid'
