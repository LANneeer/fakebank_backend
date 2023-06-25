from rest_framework import serializers
from payments.models import Invoice, Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    payment_url = serializers.URLField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)
    receipt = ReceiptSerializer(source='receipts', many=True)

    class Meta:
        model = Invoice
        fields = '__all__'

