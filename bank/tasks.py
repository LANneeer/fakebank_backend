from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from payments.models import Invoice


@shared_task
def check_invoice_expiration():
    now = timezone.now()
    expired_invoices = Invoice.objects.filter(Q(expiration_date__date__lte=now), status='pending')
    for invoice in expired_invoices:
        invoice.status = 'canceled'
        invoice.save()
