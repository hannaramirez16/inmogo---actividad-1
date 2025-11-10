from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 
                  'rol', 'telefono', 'direccion', 'documento_identidad', 
                  'fecha_nacimiento', 'foto_perfil', 'activo', 'creado_en']
        read_only_fields = ['id', 'creado_en']
    
    def create(self, validated_data):
        usuario = Usuario.objects.create_user(**validated_data)
        return usuario
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        usuario = super().update(instance, validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario

class UsuarioListSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre_completo', 'email', 'rol', 'telefono', 'activo']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or obj.username