from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet, RenovacionContratoViewSet

router = DefaultRouter()
router.register(r'contratos', ContratoViewSet, basename='contrato')
router.register(r'renovaciones', RenovacionContratoViewSet, basename='renovacion')

urlpatterns = [
    path('', include(router.urls)),
]