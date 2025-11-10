from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacion, ConfiguracionNotificacion
from .serializers import (
    NotificacionSerializer,
    NotificacionListSerializer,
    ConfiguracionNotificacionSerializer
)

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificacionListSerializer
        return NotificacionSerializer
    
    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Lista notificaciones no leídas del usuario"""
        # En producción, filtrar por request.user
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        notificaciones = self.queryset.filter(usuario_id=usuario_id, leida=False)
        serializer = NotificacionListSerializer(notificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def contador_no_leidas(self, request):
        """Contador de notificaciones no leídas"""
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        count = self.queryset.filter(usuario_id=usuario_id, leida=False).count()
        return Response({'no_leidas': count})
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """Marca una notificación como leída"""
        notificacion = self.get_object()
        notificacion.marcar_leida()
        serializer = self.get_serializer(notificacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """Marca todas las notificaciones del usuario como leídas"""
        usuario_id = request.data.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        notificaciones = self.queryset.filter(usuario_id=usuario_id, leida=False)
        count = notificaciones.count()
        
        for notif in notificaciones:
            notif.marcar_leida()
        
        return Response({
            'mensaje': f'{count} notificaciones marcadas como leídas',
            'count': count
        })
    
    @action(detail=False, methods=['delete'])
    def eliminar_leidas(self, request):
        """Elimina todas las notificaciones leídas del usuario"""
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        count, _ = self.queryset.filter(usuario_id=usuario_id, leida=True).delete()
        
        return Response({
            'mensaje': f'{count} notificaciones eliminadas',
            'count': count
        })


class ConfiguracionNotificacionViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionNotificacion.objects.all()
    serializer_class = ConfiguracionNotificacionSerializer
    
    @action(detail=False, methods=['get'])
    def mi_configuracion(self, request):
        """Obtiene la configuración del usuario actual"""
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Se requiere usuario_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            config = ConfiguracionNotificacion.objects.get(usuario_id=usuario_id)
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        except ConfiguracionNotificacion.DoesNotExist:
            # Crear configuración por defecto
            from appUsuarios.models import Usuario
            usuario = Usuario.objects.get(id=usuario_id)
            config = ConfiguracionNotificacion.objects.create(usuario=usuario)
            serializer = self.get_serializer(config)
            return Response(serializer.data, status=status.HTTP_201_CREATED)