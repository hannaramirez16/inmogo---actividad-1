from rest_framework import serializers
from .models import Archivo

class ArchivoSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    
    class Meta:
        model = Archivo
        fields = ['id', 'archivo', 'nombre_original', 'tipo', 'tamano', 'url', 'creado_en']
        read_only_fields = ['id', 'usuario', 'tamano', 'creado_en']
    
    def validate_archivo(self, value):
        """Valida el archivo subido"""
        # Validar tamaño (5MB máximo)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("El archivo no puede ser mayor a 5MB")
        
        # Validar extensiones permitidas
        extensiones_permitidas = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']
        ext = value.name.split('.')[-1].lower()
        
        if ext not in extensiones_permitidas:
            raise serializers.ValidationError(
                f"Extensión no permitida. Use: {', '.join(extensiones_permitidas)}"
            )
        
        return value