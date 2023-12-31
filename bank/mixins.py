from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=True,
    )

    class Meta:
        abstract = True
