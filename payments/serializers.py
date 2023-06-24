from rest_framework import serializers
from payments.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    payment_url = serializers.URLField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

