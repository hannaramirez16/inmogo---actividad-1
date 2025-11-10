from django.db import models
from appUsuarios.models import Usuario
from django.utils import timezone

class Notificacion(models.Model):
    TIPOS = [
        ('info', 'Información'),
        ('advertencia', 'Advertencia'),
        ('urgente', 'Urgente'),
        ('recordatorio', 'Recordatorio'),
        ('pago', 'Pago'),
        ('contrato', 'Contrato'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    # Relaciones
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    
    # Información de la notificación
    tipo = models.CharField(max_length=20, choices=TIPOS, default='info')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    
    # Enlaces
    url = models.URLField(blank=True, null=True, help_text="URL relacionada con la notificación")
    referencia_tipo = models.CharField(max_length=50, blank=True, null=True, 
                                        help_text="Tipo de objeto relacionado (contrato, pago, etc.)")
    referencia_id = models.IntegerField(blank=True, null=True, 
                                         help_text="ID del objeto relacionado")
    
    # Estado
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    creada_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notificaciones'
        ordering = ['-creada_en']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        indexes = [
            models.Index(fields=['usuario', 'leida']),
            models.Index(fields=['tipo']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_leida(self):
        """Marca la notificación como leída"""
        if not self.leida:
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save()


class ConfiguracionNotificacion(models.Model):
    """Configuración de notificaciones por usuario"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='config_notificaciones')
    
    # Tipos de notificaciones habilitadas
    notif_pagos = models.BooleanField(default=True, verbose_name="Notificaciones de pagos")
    notif_contratos = models.BooleanField(default=True, verbose_name="Notificaciones de contratos")
    notif_mantenimiento = models.BooleanField(default=True, verbose_name="Notificaciones de mantenimiento")
    notif_recordatorios = models.BooleanField(default=True, verbose_name="Recordatorios")
    
    # Canales de notificación
    notif_email = models.BooleanField(default=True, verbose_name="Notificaciones por email")
    notif_push = models.BooleanField(default=True, verbose_name="Notificaciones push")
    
    # Timestamps
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'configuraciones_notificaciones'
        verbose_name = 'Configuración de Notificación'
        verbose_name_plural = 'Configuraciones de Notificaciones'
    
    def __str__(self):
        return f"Config Notificaciones - {self.usuario.username}"