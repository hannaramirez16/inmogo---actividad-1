from rest_framework import serializers
from .models import Notificacion, ConfiguracionNotificacion
from appUsuarios.serializers import UsuarioListSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioListSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = '__all__'
        read_only_fields = ['creada_en', 'fecha_lectura']


class NotificacionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo', 'titulo', 'mensaje', 'leida', 'creada_en', 'url']


class ConfiguracionNotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionNotificacion
        fields = '__all__'
        read_only_fields = ['creada_en', 'actualizada_en']