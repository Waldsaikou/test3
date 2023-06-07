from operator import imod
from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework import routers
from .views import *
#indica ruta de llamado del api

router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)
router.register('tipoproducto', TipoProductoViewSet)
router.register('usuario', UsuarioViewSet)
router.register('tipoUsuario', TipoUsuarioViewSet)
router.register('suscripcion', SuscripcionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]