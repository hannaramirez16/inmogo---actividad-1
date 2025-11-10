from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('appUsuarios.urls')),
    path('api/inmuebles/', include('appInmuebles.urls')),
    path('api/contratos/', include('appContratos.urls')),
    path('api/pagos/', include('appPagos.urls')),
    path('api/mantenimiento/', include('appMantenimiento.urls')),
    path('api/notificaciones/', include('appNotificaciones.urls')),
    path('api/uploads/', include('appUploads.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)