from django.contrib import admin
from .models import SolicitudMantenimiento, SeguimientoMantenimiento

class SeguimientoMantenimientoInline(admin.TabularInline):
    model = SeguimientoMantenimiento
    extra = 0
    readonly_fields = ['fecha_seguimiento']
    can_delete = False


@admin.register(SolicitudMantenimiento)
class SolicitudMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['numero_solicitud', 'titulo', 'categoria', 'prioridad', 'estado', 
                    'solicitante', 'fecha_solicitud']
    list_filter = ['estado', 'prioridad', 'categoria', 'fecha_solicitud']
    search_fields = ['numero_solicitud', 'titulo', 'descripcion', 'solicitante__first_name']
    readonly_fields = ['creado_en', 'actualizado_en', 'tiempo_respuesta', 'tiempo_resolucion']
    inlines = [SeguimientoMantenimientoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero_solicitud', 'inmueble', 'contrato', 'solicitante', 'asignado_a')
        }),
        ('Detalles de la Solicitud', {
            'fields': ('categoria', 'titulo', 'descripcion', 'ubicacion_especifica')
        }),
        ('Estado y Prioridad', {
            'fields': ('prioridad', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_programada', 'fecha_inicio', 'fecha_finalizacion')
        }),
        ('Costos', {
            'fields': ('costo_estimado', 'costo_real')
        }),
        ('Archivos', {
            'fields': ('fotos', 'documentos')
        }),
        ('Observaciones y Solución', {
            'fields': ('observaciones_solicitante', 'observaciones_tecnico', 'solucion_aplicada')
        }),
        ('Calificación', {
            'fields': ('calificacion', 'comentario_calificacion')
        }),
        ('Información del Sistema', {
            'fields': ('tiempo_respuesta', 'tiempo_resolucion', 'creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SeguimientoMantenimiento)
class SeguimientoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['solicitud', 'usuario', 'estado_anterior', 'estado_nuevo', 'fecha_seguimiento']
    list_filter = ['estado_nuevo', 'fecha_seguimiento']
    search_fields = ['solicitud__numero_solicitud', 'descripcion']
    readonly_fields = ['fecha_seguimiento']