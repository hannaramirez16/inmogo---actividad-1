from django.contrib import admin
from .models import Archivo

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre_original', 'tipo', 'usuario', 'tamano', 'creado_en']
    list_filter = ['tipo', 'creado_en']
    search_fields = ['nombre_original', 'usuario__username']
    readonly_fields = ['creado_en', 'tamano', 'url']