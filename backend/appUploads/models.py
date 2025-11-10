from django.db import models
from appUsuarios.models import Usuario
import os
import uuid

def upload_to(instance, filename):
    """Genera un nombre único para el archivo"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(instance.tipo, filename)

class Archivo(models.Model):
    TIPOS = [
        ('foto_perfil', 'Foto de Perfil'),
        ('foto_inmueble', 'Foto de Inmueble'),
        ('foto_mantenimiento', 'Foto de Mantenimiento'),
        ('documento_contrato', 'Documento de Contrato'),
        ('comprobante_pago', 'Comprobante de Pago'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=upload_to)
    nombre_original = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    tamano = models.IntegerField(help_text="Tamaño en bytes")
    
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'archivos'
        ordering = ['-creado_en']
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
    
    def __str__(self):
        return f"{self.nombre_original} - {self.usuario.username}"
    
    @property
    def url(self):
        return self.archivo.url if self.archivo else None