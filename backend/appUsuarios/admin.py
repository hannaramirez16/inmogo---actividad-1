from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'activo']
    list_filter = ['rol', 'activo', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'documento_identidad']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'telefono', 'direccion', 'documento_identidad', 
                       'fecha_nacimiento', 'foto_perfil', 'activo')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'telefono', 'direccion', 'documento_identidad')
        }),
    )