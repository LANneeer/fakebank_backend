from rest_framework import viewsets
from payments.models import Invoice
from payments.serializers import InvoiceSerializer
from rest_framework.response import Response
from rest_framework import status


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

<<<<<<< Updated upstream
    def create(self, request, *args, **kwargs):
        invoice = Invoice.objects.create(**request.data)
        response_data = {
            'id': invoice.id,
            'payment_url': invoice.payment_url,
            'created_at': invoice.created_at,
            'paid_at': invoice.paid_at,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        ...
=======
    
>>>>>>> Stashed changes
