from rest_framework import serializers
from .models import CuentaCobro, Pago, EstadoCuenta
from appUsuarios.serializers import UsuarioListSerializer
from appContratos.serializers import ContratoListSerializer

class CuentaCobroSerializer(serializers.ModelSerializer):
    inquilino_detalle = UsuarioListSerializer(source='inquilino', read_only=True)
    contrato_detalle = ContratoListSerializer(source='contrato', read_only=True)
    valor_pendiente = serializers.ReadOnlyField()
    esta_vencida = serializers.ReadOnlyField()
    
    class Meta:
        model = CuentaCobro
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en', 'valor_mora']


class CuentaCobroListSerializer(serializers.ModelSerializer):
    inquilino_nombre = serializers.CharField(source='inquilino.get_full_name', read_only=True)
    valor_pendiente = serializers.ReadOnlyField()
    
    class Meta:
        model = CuentaCobro
        fields = ['id', 'numero_cuenta', 'inquilino_nombre', 'concepto', 'fecha_vencimiento', 
                  'valor_total', 'valor_pagado', 'valor_pendiente', 'estado']


class PagoSerializer(serializers.ModelSerializer):
    inquilino_detalle = UsuarioListSerializer(source='inquilino', read_only=True)
    cuenta_cobro_detalle = CuentaCobroListSerializer(source='cuenta_cobro', read_only=True)
    aprobado_por_detalle = UsuarioListSerializer(source='aprobado_por', read_only=True)
    
    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en', 'fecha_aprobacion', 'aprobado_por']


class PagoListSerializer(serializers.ModelSerializer):
    inquilino_nombre = serializers.CharField(source='inquilino.get_full_name', read_only=True)
    
    class Meta:
        model = Pago
        fields = ['id', 'numero_comprobante', 'inquilino_nombre', 'fecha_pago', 
                  'monto', 'metodo_pago', 'estado']


class EstadoCuentaSerializer(serializers.ModelSerializer):
    contrato_detalle = ContratoListSerializer(source='contrato', read_only=True)
    
    class Meta:
        model = EstadoCuenta
        fields = '__all__'