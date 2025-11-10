from django.contrib import admin
from .models import Notificacion, ConfiguracionNotificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo', 'leida', 'creada_en']
    list_filter = ['tipo', 'leida', 'creada_en']
    search_fields = ['titulo', 'mensaje', 'usuario__username', 'usuario__email']
    readonly_fields = ['creada_en', 'fecha_lectura']
    
    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'tipo', 'titulo', 'mensaje')
        }),
        ('Referencias', {
            'fields': ('url', 'referencia_tipo', 'referencia_id')
        }),
        ('Estado', {
            'fields': ('leida', 'fecha_lectura', 'creada_en')
        }),
    )


@admin.register(ConfiguracionNotificacion)
class ConfiguracionNotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'notif_pagos', 'notif_contratos', 'notif_mantenimiento', 
                    'notif_email', 'notif_push']
    list_filter = ['notif_email', 'notif_push']
    search_fields = ['usuario__username', 'usuario__email']
    readonly_fields = ['creada_en', 'actualizada_en']