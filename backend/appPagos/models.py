from django.db import models
from appContratos.models import Contrato
from appUsuarios.models import Usuario
from django.utils import timezone

class CuentaCobro(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('parcial', 'Pago Parcial'),
    ]
    
    CONCEPTOS = [
        ('arriendo', 'Arriendo'),
        ('administracion', 'Administración'),
        ('servicios', 'Servicios'),
        ('mora', 'Mora'),
        ('reparacion', 'Reparación'),
        ('otro', 'Otro'),
    ]
    
    # Relaciones
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='cuentas_cobro')
    inquilino = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='cuentas_cobro')
    
    # Información de la cuenta
    numero_cuenta = models.CharField(max_length=50, unique=True)
    concepto = models.CharField(max_length=50, choices=CONCEPTOS, default='arriendo')
    descripcion = models.TextField(blank=True, null=True)
    
    # Fechas
    fecha_emision = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField()
    periodo_inicio = models.DateField(help_text="Inicio del período facturado")
    periodo_fin = models.DateField(help_text="Fin del período facturado")
    
    # Valores
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porcentaje_mora = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    # Documentos
    documento_url = models.URLField(blank=True, null=True, help_text="URL del PDF de cuenta de cobro")
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cuentas_cobro'
        ordering = ['-fecha_emision']
        verbose_name = 'Cuenta de Cobro'
        verbose_name_plural = 'Cuentas de Cobro'
        indexes = [
            models.Index(fields=['estado', 'fecha_vencimiento']),
            models.Index(fields=['contrato']),
            models.Index(fields=['inquilino']),
        ]
    
    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - {self.inquilino.get_full_name()}"
    
    @property
    def valor_pendiente(self):
        """Calcula el valor pendiente de pago"""
        return self.valor_total - self.valor_pagado + self.valor_mora
    
    @property
    def esta_vencida(self):
        """Verifica si la cuenta está vencida"""
        return timezone.now().date() > self.fecha_vencimiento and self.estado == 'pendiente'
    
    def calcular_mora(self):
        """Calcula el valor de la mora si está vencida"""
        if self.esta_vencida and self.valor_pendiente > 0:
            dias_mora = (timezone.now().date() - self.fecha_vencimiento).days
            # Mora por día basada en el porcentaje configurado
            mora_diaria = (self.valor_pendiente * self.porcentaje_mora / 100) / 30
            self.valor_mora = mora_diaria * dias_mora
            self.estado = 'vencida'
            self.save()
    
    def registrar_pago(self, monto):
        """Registra un pago hacia esta cuenta"""
        self.valor_pagado += monto
        if self.valor_pagado >= self.valor_total + self.valor_mora:
            self.estado = 'pagada'
        elif self.valor_pagado > 0:
            self.estado = 'parcial'
        self.save()


class Pago(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('cheque', 'Cheque'),
        ('pse', 'PSE'),
        ('otro', 'Otro'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    # Relaciones
    cuenta_cobro = models.ForeignKey(CuentaCobro, on_delete=models.PROTECT, related_name='pagos')
    inquilino = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pagos')
    
    # Información del pago
    numero_comprobante = models.CharField(max_length=50, unique=True)
    fecha_pago = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)
    
    # Valores
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Referencia bancaria
    referencia_bancaria = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    
    # Estado y documentos
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    comprobante_url = models.URLField(blank=True, null=True, help_text="URL del comprobante de pago")
    observaciones = models.TextField(blank=True, null=True)
    
    # Aprobación
    aprobado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='pagos_aprobados')
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_pago']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        indexes = [
            models.Index(fields=['estado', 'fecha_pago']),
            models.Index(fields=['cuenta_cobro']),
        ]
    
    def __str__(self):
        return f"Pago {self.numero_comprobante} - ${self.monto}"
    
    def aprobar(self, usuario):
        """Aprueba el pago y actualiza la cuenta de cobro"""
        self.estado = 'aprobado'
        self.aprobado_por = usuario
        self.fecha_aprobacion = timezone.now()
        self.save()
        
        # Registrar el pago en la cuenta de cobro
        self.cuenta_cobro.registrar_pago(self.monto)
    
    def rechazar(self, observaciones=None):
        """Rechaza el pago"""
        self.estado = 'rechazado'
        if observaciones:
            self.observaciones = observaciones
        self.save()


class EstadoCuenta(models.Model):
    """Estado de cuenta mensual de un contrato"""
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='estados_cuenta')
    
    periodo_mes = models.IntegerField()
    periodo_ano = models.IntegerField()
    
    total_facturado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    documento_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'estados_cuenta'
        ordering = ['-periodo_ano', '-periodo_mes']
        verbose_name = 'Estado de Cuenta'
        verbose_name_plural = 'Estados de Cuenta'
        unique_together = ['contrato', 'periodo_mes', 'periodo_ano']
    
    def __str__(self):
        return f"Estado de Cuenta {self.periodo_mes}/{self.periodo_ano} - Contrato {self.contrato.numero_contrato}"