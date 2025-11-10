from django.contrib import admin
from .models import Contrato, RenovacionContrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['numero_contrato', 'inquilino', 'inmueble', 'fecha_inicio', 'fecha_fin', 'estado', 'valor_arriendo']
    list_filter = ['estado', 'fecha_inicio', 'fecha_fin']
    search_fields = ['numero_contrato', 'inquilino__first_name', 'inquilino__last_name', 'inmueble__titulo']
    readonly_fields = ['creado_en', 'actualizado_en', 'dias_restantes', 'valor_total_mensual']
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero_contrato', 'inmueble', 'inquilino', 'propietario', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'duracion_meses', 'dia_pago')
        }),
        ('Valores Económicos', {
            'fields': ('valor_arriendo', 'valor_administracion', 'deposito_garantia', 'porcentaje_incremento')
        }),
        ('Documentación', {
            'fields': ('documento_contrato_url', 'clausulas_especiales', 'observaciones')
        }),
        ('Información del Sistema', {
            'fields': ('creado_en', 'actualizado_en', 'fecha_finalizacion', 'dias_restantes', 'valor_total_mensual'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RenovacionContrato)
class RenovacionContratoAdmin(admin.ModelAdmin):
    list_display = ['contrato_original', 'contrato_nuevo', 'fecha_renovacion', 'nuevo_valor_arriendo']
    list_filter = ['fecha_renovacion']
    search_fields = ['contrato_original__numero_contrato', 'contrato_nuevo__numero_contrato']