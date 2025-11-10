from rest_framework import serializers
from .models import SolicitudMantenimiento, SeguimientoMantenimiento
from appUsuarios.serializers import UsuarioListSerializer
from appInmuebles.serializers import InmuebleListSerializer

class SeguimientoMantenimientoSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioListSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = SeguimientoMantenimiento
        fields = '__all__'
        read_only_fields = ['fecha_seguimiento']


class SolicitudMantenimientoSerializer(serializers.ModelSerializer):
    solicitante_detalle = UsuarioListSerializer(source='solicitante', read_only=True)
    asignado_a_detalle = UsuarioListSerializer(source='asignado_a', read_only=True)
    inmueble_detalle = InmuebleListSerializer(source='inmueble', read_only=True)
    seguimientos = SeguimientoMantenimientoSerializer(many=True, read_only=True)
    tiempo_respuesta = serializers.ReadOnlyField()
    tiempo_resolucion = serializers.ReadOnlyField()
    
    class Meta:
        model = SolicitudMantenimiento
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en']


class SolicitudMantenimientoListSerializer(serializers.ModelSerializer):
    solicitante_nombre = serializers.CharField(source='solicitante.get_full_name', read_only=True)
    inmueble_titulo = serializers.CharField(source='inmueble.titulo', read_only=True)
    
    class Meta:
        model = SolicitudMantenimiento
        fields = ['id', 'numero_solicitud', 'titulo', 'categoria', 'prioridad', 
                  'estado', 'solicitante_nombre', 'inmueble_titulo', 'fecha_solicitud']