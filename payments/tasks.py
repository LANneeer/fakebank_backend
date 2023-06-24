from celery import shared_task
from django.utils import timezone
from .models import Invoice


@shared_task
def check_invoice_expiration():
    now = timezone.now()
    expired_invoices = Invoice.objects.filter(expiration_date__lte=now, status='active')

    for invoice in expired_invoices:
        invoice.status = 'canceled'
        invoice.save()
