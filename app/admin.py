from django.contrib import admin
from .models import *

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display=['rut','nombre','apellido','contraseña','comuna','direccion','tipo']
    search_fields=['rut']
    list_per_page=5

class ProductoAdmin(admin.ModelAdmin):
    list_display=['codigo','nombre','raza','stock','descripcion','precio','tipo','image_tag','created_at']
    search_fields=['codigo']
    readonly_fields = ['image_tag']
    list_per_page=5

class ItemsAdmin(admin.ModelAdmin):
    list_display=['id_carro','nombre_producto','precio_producto','imagen']
    search_fields=['nombre_producto']
    list_per_page=5

class SuscripcionAdmin(admin.ModelAdmin):
    list_display=['id_suscripcion','suscripcion','usuario']
    search_fields=['usuario']
    list_per_page=5

class HistorialAdmin(admin.ModelAdmin):
    list_display=['id_historial','nombre_historial','precio_historial','imagen_historial']
    search_fields=['id_historial']
    list_per_page=5
admin.site.register(TipoProducto)
admin.site.register(TipoUsuario)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Items_Carrito,ItemsAdmin)
admin.site.register(Suscripcion,SuscripcionAdmin)
admin.site.register(Historial,HistorialAdmin)