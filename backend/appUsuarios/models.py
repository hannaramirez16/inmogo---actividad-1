from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('propietario', 'Propietario'),
        ('inquilino', 'Inquilino'),
        ('admin', 'Administrador'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='inquilino')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    documento_identidad = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    # Solución al conflicto de reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',  # <- AGREGAR ESTO
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',  # <- AGREGAR ESTO
        related_query_name='usuario',
    )
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_rol_display()}"