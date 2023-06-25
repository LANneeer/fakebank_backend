import httpx
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models import Invoice
from payments.serializers import InvoiceSerializer
from payments.utils import status_changed_notify


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        invoice = Invoice.objects.create(**request.data)
        invoice.payment_url = f'api/billing/{invoice.id}'
        response_data = {
            'id': invoice.id,
            'payment_url': invoice.payment_url,
            'created_at': invoice.created_at,
            'paid_at': invoice.paid_at,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.data['status'] == 'canceled' or request.data['status'] == 'paid':
            invoice = Invoice.objects.get(id=kwargs['pk'])
            print(request.data['status'])
            status_changed_notify(callback_url=invoice.callback_url, callback_data=invoice.callback_data)
        return super().update(request=request, *args, **kwargs)


class BillingViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=kwargs['pk'])
        payload = {'callback_url': invoice.callback_url, 'callback_data': invoice.callback_data}
        return Response(template_name='index.html', data=payload)


class CallbackViewSet(viewsets.ViewSet):
    def post_callback(self, request, *args, **kwargs):
        response = httpx.post(url=request.data['callback_url'], data={'callback_data': request.data['callback_data']})
        return Response(status=response.status_code)
