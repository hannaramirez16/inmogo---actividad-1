from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificacionViewSet, ConfiguracionNotificacionViewSet  # <- CORRECTO

router = DefaultRouter()
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')
router.register(r'configuraciones', ConfiguracionNotificacionViewSet, basename='configuracion')

urlpatterns = [
    path('', include(router.urls)),
]