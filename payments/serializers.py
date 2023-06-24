from rest_framework import serializers
from payments.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    payment_url = serializers.URLField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        invoice = Invoice.objects.create(**validated_data)
        response_data = {
            'id': invoice.id,
            'payment_url': invoice.payment_url,
            'created_at': invoice.created_at,
            'paid_at': invoice.paid_at,
        }
        return response_data

    class Meta:
        model = Invoice
        fields = '__all__'

