from django.contrib import admin
from payments.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'paid_at', 'expiration_date')
    list_filter = ('status', 'paid_at', 'expiration_date')
    search_fields = ('id', 'amount', 'status')
    readonly_fields = ('id', 'paid_at')
