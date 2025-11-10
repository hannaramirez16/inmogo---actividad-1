from django.db import models
from appUsuarios.models import Usuario

class CategoriaInmueble(models.Model):
    TIPOS = [
        ('terreno', 'Terreno'),
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('local_comercial', 'Local Comercial'),
        ('oficina', 'Oficina'),
        ('bodega', 'Bodega'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=50, choices=TIPOS, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categorias_inmuebles'
        verbose_name = 'Categoría de Inmueble'
        verbose_name_plural = 'Categorías de Inmuebles'
    
    def __str__(self):
        return self.get_nombre_display()


class Inmueble(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('no_disponible', 'No Disponible'),
    ]
    
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inmuebles')
    categoria = models.ForeignKey(CategoriaInmueble, on_delete=models.PROTECT, related_name='inmuebles')
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    
    area_construida = models.DecimalField(max_digits=10, decimal_places=2, help_text="Metros cuadrados")
    area_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Metros cuadrados", blank=True, null=True)
    
    num_habitaciones = models.IntegerField(default=0)
    num_banos = models.IntegerField(default=0)
    num_parqueaderos = models.IntegerField(default=0)
    piso = models.IntegerField(blank=True, null=True)
    
    precio_arriendo = models.DecimalField(max_digits=12, decimal_places=2)
    precio_administracion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposito_garantia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    amoblado = models.BooleanField(default=False)
    permite_mascotas = models.BooleanField(default=False)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    
    fotos = models.JSONField(default=list, blank=True, help_text="URLs de las fotos")
    caracteristicas = models.JSONField(default=dict, blank=True, help_text="Características adicionales")
    
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inmuebles'
        ordering = ['-creado_en']
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'
        indexes = [
            models.Index(fields=['estado', 'ciudad']),
            models.Index(fields=['propietario']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.direccion}"


class MuebleInmueble(models.Model):
    """Inventario de muebles incluidos en un inmueble"""
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='muebles')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    estado = models.CharField(max_length=50, choices=[
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
    ], default='bueno')
    foto = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'muebles_inmuebles'
        verbose_name = 'Mueble de Inmueble'
        verbose_name_plural = 'Muebles de Inmuebles'
    
    def __str__(self):
        return f"{self.nombre} - {self.inmueble.titulo}"