from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import SolicitudMantenimiento, SeguimientoMantenimiento
from .serializers import (
    SolicitudMantenimientoSerializer,
    SolicitudMantenimientoListSerializer,
    SeguimientoMantenimientoSerializer
)

class SolicitudMantenimientoViewSet(viewsets.ModelViewSet):
    queryset = SolicitudMantenimiento.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SolicitudMantenimientoListSerializer
        return SolicitudMantenimientoSerializer
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Lista solicitudes pendientes"""
        solicitudes = self.queryset.filter(estado='pendiente')
        serializer = SolicitudMantenimientoListSerializer(solicitudes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgentes(self, request):
        """Lista solicitudes urgentes"""
        solicitudes = self.queryset.filter(prioridad='urgente', estado__in=['pendiente', 'en_revision', 'aprobada'])
        serializer = SolicitudMantenimientoListSerializer(solicitudes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def en_progreso(self, request):
        """Lista solicitudes en progreso"""
        solicitudes = self.queryset.filter(estado='en_progreso')
        serializer = SolicitudMantenimientoListSerializer(solicitudes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def asignar(self, request, pk=None):
        """Asigna un técnico a la solicitud"""
        solicitud = self.get_object()
        usuario_id = request.data.get('usuario_id')
        
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        from appUsuarios.models import Usuario
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            estado_anterior = solicitud.estado
            solicitud.asignado_a = usuario
            solicitud.estado = 'aprobada'
            solicitud.save()
            
            # Crear seguimiento
            SeguimientoMantenimiento.objects.create(
                solicitud=solicitud,
                usuario=request.user if request.user.is_authenticated else usuario,
                estado_anterior=estado_anterior,
                estado_nuevo='aprobada',
                descripcion=f"Solicitud asignada a {usuario.get_full_name()}"
            )
            
            serializer = self.get_serializer(solicitud)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Inicia el trabajo de mantenimiento"""
        solicitud = self.get_object()
        estado_anterior = solicitud.estado
        solicitud.estado = 'en_progreso'
        solicitud.fecha_inicio = timezone.now()
        solicitud.save()
        
        # Crear seguimiento
        SeguimientoMantenimiento.objects.create(
            solicitud=solicitud,
            usuario=request.user if request.user.is_authenticated else solicitud.asignado_a,
            estado_anterior=estado_anterior,
            estado_nuevo='en_progreso',
            descripcion="Inicio del trabajo de mantenimiento"
        )
        
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Completa el trabajo de mantenimiento"""
        solicitud = self.get_object()
        estado_anterior = solicitud.estado
        
        solicitud.estado = 'completada'
        solicitud.fecha_finalizacion = timezone.now()
        solicitud.solucion_aplicada = request.data.get('solucion_aplicada', '')
        solicitud.costo_real = request.data.get('costo_real', solicitud.costo_estimado)
        solicitud.save()
        
        # Crear seguimiento
        SeguimientoMantenimiento.objects.create(
            solicitud=solicitud,
            usuario=request.user if request.user.is_authenticated else solicitud.asignado_a,
            estado_anterior=estado_anterior,
            estado_nuevo='completada',
            descripcion=f"Trabajo completado. {solicitud.solucion_aplicada}"
        )
        
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def calificar(self, request, pk=None):
        """Califica el servicio de mantenimiento"""
        solicitud = self.get_object()
        
        calificacion = request.data.get('calificacion')
        comentario = request.data.get('comentario', '')
        
        if not calificacion or not (1 <= int(calificacion) <= 5):
            return Response({'error': 'La calificación debe ser entre 1 y 5'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.calificacion = calificacion
        solicitud.comentario_calificacion = comentario
        solicitud.save()
        
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def agregar_seguimiento(self, request, pk=None):
        """Agrega un seguimiento a la solicitud"""
        solicitud = self.get_object()
        
        descripcion = request.data.get('descripcion')
        fotos = request.data.get('fotos', [])
        
        if not descripcion:
            return Response({'error': 'Se requiere una descripción'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        seguimiento = SeguimientoMantenimiento.objects.create(
            solicitud=solicitud,
            usuario=request.user if request.user.is_authenticated else solicitud.asignado_a,
            estado_anterior=solicitud.estado,
            estado_nuevo=solicitud.estado,
            descripcion=descripcion,
            fotos=fotos
        )
        
        serializer = SeguimientoMantenimientoSerializer(seguimiento)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SeguimientoMantenimientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeguimientoMantenimiento.objects.all()
    serializer_class = SeguimientoMantenimientoSerializer