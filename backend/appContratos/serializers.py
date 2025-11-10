from rest_framework import serializers
from .models import Contrato, RenovacionContrato
from appUsuarios.serializers import UsuarioListSerializer
from appInmuebles.serializers import InmuebleListSerializer

class ContratoSerializer(serializers.ModelSerializer):
    inquilino_detalle = UsuarioListSerializer(source='inquilino', read_only=True)
    propietario_detalle = UsuarioListSerializer(source='propietario', read_only=True)
    inmueble_detalle = InmuebleListSerializer(source='inmueble', read_only=True)
    dias_restantes = serializers.ReadOnlyField()
    valor_total_mensual = serializers.ReadOnlyField()
    
    class Meta:
        model = Contrato
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en', 'fecha_finalizacion']
    
    def validate(self, data):
        """Validaciones personalizadas"""
        if data.get('fecha_inicio') and data.get('fecha_fin'):
            if data['fecha_inicio'] >= data['fecha_fin']:
                raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        if data.get('inquilino') and data.get('inquilino').rol != 'inquilino':
            raise serializers.ValidationError("El usuario seleccionado debe tener rol de inquilino")
        
        if data.get('propietario') and data.get('propietario').rol != 'propietario':
            raise serializers.ValidationError("El usuario seleccionado debe tener rol de propietario")
        
        return data


class ContratoListSerializer(serializers.ModelSerializer):
    inquilino_nombre = serializers.CharField(source='inquilino.get_full_name', read_only=True)
    inmueble_titulo = serializers.CharField(source='inmueble.titulo', read_only=True)
    dias_restantes = serializers.ReadOnlyField()
    
    class Meta:
        model = Contrato
        fields = ['id', 'numero_contrato', 'inquilino_nombre', 'inmueble_titulo', 
                  'fecha_inicio', 'fecha_fin', 'valor_arriendo', 'estado', 'dias_restantes']


class RenovacionContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenovacionContrato
        fields = '__all__'