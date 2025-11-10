from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from backend.permissions import IsPropietario, IsOwnerOrReadOnly
from .models import CategoriaInmueble, Inmueble, MuebleInmueble
from .serializers import (
    CategoriaInmuebleSerializer, 
    InmuebleSerializer, 
    InmuebleListSerializer,
    MuebleInmuebleSerializer
)

class CategoriaInmuebleViewSet(viewsets.ModelViewSet):
    queryset = CategoriaInmueble.objects.filter(activo=True)
    serializer_class = CategoriaInmuebleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'estado', 'ciudad', 'propietario', 'amoblado', 'permite_mascotas']
    search_fields = ['titulo', 'descripcion', 'direccion', 'ciudad']
    ordering_fields = ['precio_arriendo', 'creado_en', 'area_construida']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InmuebleListSerializer
        return InmuebleSerializer
    
    def perform_create(self, serializer):
        """Asigna automáticamente el propietario al usuario actual"""
        serializer.save(propietario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mis_inmuebles(self, request):
        """Lista los inmuebles del usuario actual (propietario)"""
        inmuebles = self.queryset.filter(propietario=request.user)
        serializer = InmuebleListSerializer(inmuebles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Lista inmuebles disponibles para arrendar"""
        inmuebles = self.queryset.filter(estado='disponible')
        serializer = InmuebleListSerializer(inmuebles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def muebles(self, request, pk=None):
        """Lista los muebles de un inmueble específico"""
        inmueble = self.get_object()
        muebles = inmueble.muebles.all()
        serializer = MuebleInmuebleSerializer(muebles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def agregar_mueble(self, request, pk=None):
        """Agrega un mueble a un inmueble"""
        inmueble = self.get_object()
        serializer = MuebleInmuebleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(inmueble=inmueble)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MuebleInmuebleViewSet(viewsets.ModelViewSet):
    queryset = MuebleInmueble.objects.all()
    serializer_class = MuebleInmuebleSerializer
    permission_classes = [IsAuthenticated]