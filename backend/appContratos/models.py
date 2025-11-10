from django.db import models
from appUsuarios.models import Usuario
from appInmuebles.models import Inmueble
from django.utils import timezone
from datetime import timedelta

class Contrato(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('vencido', 'Vencido'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Relaciones
    inmueble = models.ForeignKey(Inmueble, on_delete=models.PROTECT, related_name='contratos')
    inquilino = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='contratos_inquilino')
    propietario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='contratos_propietario')
    
    # Información del contrato
    numero_contrato = models.CharField(max_length=50, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    duracion_meses = models.IntegerField(help_text="Duración en meses")
    
    # Valores económicos
    valor_arriendo = models.DecimalField(max_digits=12, decimal_places=2)
    valor_administracion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposito_garantia = models.DecimalField(max_digits=12, decimal_places=2)
    dia_pago = models.IntegerField(default=1, help_text="Día del mes para el pago")
    
    # Incremento anual
    porcentaje_incremento = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                                 help_text="Porcentaje de incremento anual")
    
    # Estado y documentos
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    documento_contrato_url = models.URLField(blank=True, null=True, help_text="URL del contrato PDF")
    
    # Observaciones
    clausulas_especiales = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    fecha_finalizacion = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'contratos'
        ordering = ['-fecha_inicio']
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        indexes = [
            models.Index(fields=['estado', 'fecha_fin']),
            models.Index(fields=['inquilino']),
            models.Index(fields=['inmueble']),
        ]
    
    def __str__(self):
        return f"Contrato {self.numero_contrato} - {self.inquilino.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Actualizar estado del inmueble
        if self.estado == 'activo':
            self.inmueble.estado = 'ocupado'
            self.inmueble.save()
        elif self.estado in ['finalizado', 'cancelado']:
            self.inmueble.estado = 'disponible'
            self.inmueble.save()
        super().save(*args, **kwargs)
    
    def verificar_vencimiento(self):
        """Verifica si el contrato está vencido"""
        if self.estado == 'activo' and self.fecha_fin < timezone.now().date():
            self.estado = 'vencido'
            self.save()
            return True
        return False
    
    @property
    def dias_restantes(self):
        """Calcula los días restantes del contrato"""
        if self.estado == 'activo':
            delta = self.fecha_fin - timezone.now().date()
            return delta.days if delta.days > 0 else 0
        return 0
    
    @property
    def valor_total_mensual(self):
        """Calcula el valor total mensual (arriendo + administración)"""
        return self.valor_arriendo + self.valor_administracion


class RenovacionContrato(models.Model):
    """Registro de renovaciones de contratos"""
    contrato_original = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='renovaciones')
    contrato_nuevo = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='renovacion_de')
    
    fecha_renovacion = models.DateField(auto_now_add=True)
    nuevo_valor_arriendo = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'renovaciones_contratos'
        verbose_name = 'Renovación de Contrato'
        verbose_name_plural = 'Renovaciones de Contratos'
    
    def __str__(self):
        return f"Renovación {self.contrato_original.numero_contrato} → {self.contrato_nuevo.numero_contrato}"