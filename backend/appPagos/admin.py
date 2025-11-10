from django.contrib import admin
from .models import CuentaCobro, Pago, EstadoCuenta

@admin.register(CuentaCobro)
class CuentaCobroAdmin(admin.ModelAdmin):
    list_display = ['numero_cuenta', 'inquilino', 'concepto', 'fecha_vencimiento', 'valor_total', 'valor_pagado', 'estado']
    list_filter = ['estado', 'concepto', 'fecha_vencimiento']
    search_fields = ['numero_cuenta', 'inquilino__first_name', 'inquilino__last_name']
    readonly_fields = ['creado_en', 'actualizado_en', 'valor_pendiente', 'esta_vencida']
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero_cuenta', 'contrato', 'inquilino', 'concepto', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_vencimiento', 'periodo_inicio', 'periodo_fin')
        }),
        ('Valores', {
            'fields': ('valor_total', 'valor_pagado', 'valor_mora', 'porcentaje_mora')
        }),
        ('Estado', {
            'fields': ('estado', 'documento_url')
        }),
        ('Información del Sistema', {
            'fields': ('valor_pendiente', 'esta_vencida', 'creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['numero_comprobante', 'inquilino', 'fecha_pago', 'monto', 'metodo_pago', 'estado']
    list_filter = ['estado', 'metodo_pago', 'fecha_pago']
    search_fields = ['numero_comprobante', 'inquilino__first_name', 'inquilino__last_name', 'referencia_bancaria']
    readonly_fields = ['creado_en', 'actualizado_en', 'fecha_aprobacion']
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero_comprobante', 'cuenta_cobro', 'inquilino', 'fecha_pago')
        }),
        ('Detalles del Pago', {
            'fields': ('monto', 'metodo_pago', 'referencia_bancaria', 'banco')
        }),
        ('Estado y Documentos', {
            'fields': ('estado', 'comprobante_url', 'observaciones')
        }),
        ('Aprobación', {
            'fields': ('aprobado_por', 'fecha_aprobacion')
        }),
        ('Información del Sistema', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EstadoCuenta)
class EstadoCuentaAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'periodo_mes', 'periodo_ano', 'total_facturado', 'total_pagado', 'total_pendiente']
    list_filter = ['periodo_ano', 'periodo_mes']
    search_fields = ['contrato__numero_contrato']
    readonly_fields = ['fecha_generacion']