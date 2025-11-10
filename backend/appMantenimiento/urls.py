from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudMantenimientoViewSet, SeguimientoMantenimientoViewSet

router = DefaultRouter()
router.register(r'solicitudes', SolicitudMantenimientoViewSet, basename='solicitud')
router.register(r'seguimientos', SeguimientoMantenimientoViewSet, basename='seguimiento')

urlpatterns = [
    path('', include(router.urls)),
]