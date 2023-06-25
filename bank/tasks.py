from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from payments.models import Invoice
from payments.utils import status_changed_notify

@shared_task
def check_invoice_expiration():
    now = timezone.now()
    expired_invoices = Invoice.objects.filter(Q(expiration_date__lte=now), status='pending')
    for invoice in expired_invoices:
        invoice.status = 'canceled'
        invoice.expiration_date = now + timedelta(1)
        invoice.save()
        status_changed_notify(callback_url=invoice.callback_url, callback_data=invoice.callback_data)

