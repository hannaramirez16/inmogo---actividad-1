from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaInmuebleViewSet, InmuebleViewSet, MuebleInmuebleViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaInmuebleViewSet, basename='categoria')
router.register(r'inmuebles', InmuebleViewSet, basename='inmueble')
router.register(r'muebles', MuebleInmuebleViewSet, basename='mueble')

urlpatterns = [
    path('', include(router.urls)),
]