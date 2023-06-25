from django.contrib import admin
from payments.models import Invoice, Receipt


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'paid_at', 'expiration_date')
    list_filter = ('status', 'paid_at', 'expiration_date')
    search_fields = ('id', 'amount', 'status')
    readonly_fields = ('id', 'paid_at')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'pdf_file')
    readonly_fields = ('pdf_file',)
