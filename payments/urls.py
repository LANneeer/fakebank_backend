from rest_framework.routers import DefaultRouter
from payments.views import InvoiceViewSet

router = DefaultRouter()

app_name = 'payments'

router.register('invoice', InvoiceViewSet, basename='invoice')

urlpatterns = router.urls
