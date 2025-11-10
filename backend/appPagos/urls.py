from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuentaCobroViewSet, PagoViewSet, EstadoCuentaViewSet

router = DefaultRouter()
router.register(r'cuentas-cobro', CuentaCobroViewSet, basename='cuenta-cobro')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'estados-cuenta', EstadoCuentaViewSet, basename='estado-cuenta')

urlpatterns = [
    path('', include(router.urls)),
]