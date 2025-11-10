from django.contrib import admin
from .models import CategoriaInmueble, Inmueble, MuebleInmueble

@admin.register(CategoriaInmueble)
class CategoriaInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']


class MuebleInmuebleInline(admin.TabularInline):
    model = MuebleInmueble
    extra = 1


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'propietario', 'ciudad', 'precio_arriendo', 'estado']
    list_filter = ['categoria', 'estado', 'ciudad', 'amoblado', 'permite_mascotas']
    search_fields = ['titulo', 'descripcion', 'direccion']
    readonly_fields = ['creado_en', 'actualizado_en']
    inlines = [MuebleInmuebleInline]


@admin.register(MuebleInmueble)
class MuebleInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'inmueble', 'cantidad', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre', 'inmueble__titulo']