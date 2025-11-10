from rest_framework import serializers
from .models import CategoriaInmueble, Inmueble, MuebleInmueble
from appUsuarios.serializers import UsuarioListSerializer

class CategoriaInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaInmueble
        fields = '__all__'


class MuebleInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuebleInmueble
        fields = '__all__'
        read_only_fields = ['inmueble']


class InmuebleSerializer(serializers.ModelSerializer):
    propietario_detalle = UsuarioListSerializer(source='propietario', read_only=True)
    categoria_detalle = CategoriaInmuebleSerializer(source='categoria', read_only=True)
    muebles = MuebleInmuebleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Inmueble
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en']


class InmuebleListSerializer(serializers.ModelSerializer):
    propietario_nombre = serializers.CharField(source='propietario.get_full_name', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.get_nombre_display', read_only=True)
    primera_foto = serializers.SerializerMethodField()
    
    class Meta:
        model = Inmueble
        fields = ['id', 'titulo', 'direccion', 'ciudad', 'categoria_nombre', 
                  'propietario_nombre', 'precio_arriendo', 'estado', 'num_habitaciones', 
                  'num_banos', 'area_construida', 'primera_foto', 'amoblado']
    
    def get_primera_foto(self, obj):
        if obj.fotos and len(obj.fotos) > 0:
            return obj.fotos[0]
        return None