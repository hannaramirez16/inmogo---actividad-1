from django.db import models
from appUsuarios.models import Usuario
from appInmuebles.models import Inmueble
from appContratos.models import Contrato
from django.utils import timezone

class SolicitudMantenimiento(models.Model):
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aprobada', 'Aprobada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]
    
    CATEGORIAS = [
        ('plomeria', 'Plomería'),
        ('electricidad', 'Electricidad'),
        ('pintura', 'Pintura'),
        ('carpinteria', 'Carpintería'),
        ('electrodomesticos', 'Electrodomésticos'),
        ('limpieza', 'Limpieza'),
        ('jardineria', 'Jardinería'),
        ('cerrajeria', 'Cerrajería'),
        ('aire_acondicionado', 'Aire Acondicionado'),
        ('otro', 'Otro'),
    ]
    
    # Relaciones
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='solicitudes_mantenimiento')
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='solicitudes_mantenimiento')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_mantenimiento')
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='mantenimientos_asignados')
    
    # Información de la solicitud
    numero_solicitud = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Prioridad y estado
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    # Fechas
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    
    # Ubicación específica
    ubicacion_especifica = models.CharField(max_length=200, blank=True, null=True,
                                             help_text="Ej: Baño principal, Cocina, Sala, etc.")
    
    # Costos
    costo_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Archivos adjuntos
    fotos = models.JSONField(default=list, blank=True, help_text="URLs de fotos del problema")
    documentos = models.JSONField(default=list, blank=True, help_text="URLs de documentos relacionados")
    
    # Observaciones
    observaciones_solicitante = models.TextField(blank=True, null=True)
    observaciones_tecnico = models.TextField(blank=True, null=True)
    solucion_aplicada = models.TextField(blank=True, null=True)
    
    # Calificación
    calificacion = models.IntegerField(null=True, blank=True, help_text="Calificación del servicio (1-5)")
    comentario_calificacion = models.TextField(blank=True, null=True)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'solicitudes_mantenimiento'
        ordering = ['-fecha_solicitud']
        verbose_name = 'Solicitud de Mantenimiento'
        verbose_name_plural = 'Solicitudes de Mantenimiento'
        indexes = [
            models.Index(fields=['estado', 'prioridad']),
            models.Index(fields=['inmueble']),
            models.Index(fields=['solicitante']),
        ]
    
    def __str__(self):
        return f"Solicitud {self.numero_solicitud} - {self.titulo}"
    
    @property
    def tiempo_respuesta(self):
        """Calcula el tiempo de respuesta en horas"""
        if self.fecha_inicio:
            delta = self.fecha_inicio - self.fecha_solicitud
            return round(delta.total_seconds() / 3600, 2)
        return None
    
    @property
    def tiempo_resolucion(self):
        """Calcula el tiempo de resolución en horas"""
        if self.fecha_finalizacion:
            delta = self.fecha_finalizacion - self.fecha_solicitud
            return round(delta.total_seconds() / 3600, 2)
        return None


class SeguimientoMantenimiento(models.Model):
    """Registro de seguimiento de una solicitud de mantenimiento"""
    solicitud = models.ForeignKey(SolicitudMantenimiento, on_delete=models.CASCADE, 
                                   related_name='seguimientos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    
    descripcion = models.TextField()
    fotos = models.JSONField(default=list, blank=True, help_text="URLs de fotos del seguimiento")
    
    fecha_seguimiento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'seguimientos_mantenimiento'
        ordering = ['-fecha_seguimiento']
        verbose_name = 'Seguimiento de Mantenimiento'
        verbose_name_plural = 'Seguimientos de Mantenimiento'
    
    def __str__(self):
        return f"Seguimiento {self.solicitud.numero_solicitud} - {self.fecha_seguimiento}"