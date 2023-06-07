from distutils.command.upload import upload
from statistics import mode
from django.utils.html import mark_safe
from django.db import models

# Create your models here.

class TipoProducto(models.Model):
    tipo = models.CharField(max_length=40)

    def __str__(self):
        return self.tipo
    class meta:
        db_table= 'db_tipo_producto'

class Producto(models.Model):
    codigo = models.IntegerField(null=False, primary_key=True)
    nombre = models.CharField(max_length=40)
    raza = models.CharField(max_length=40)
    stock = models.IntegerField()
    cantidad= models.IntegerField()
    descripcion = models.CharField(max_length=60)
    precio = models.IntegerField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre
    def image_tag(self):
            return mark_safe('<img src="/media/%s" width="60" />' % (self.imagen))

    image_tag.short_description = 'Imagen'

    class meta:
        db_table= 'db_producto'

class Suscripcion(models.Model):
    id_suscripcion = models.AutoField(null=False, primary_key=True)
    suscripcion = models.BooleanField(null=False)
    usuario = models.CharField(max_length=40)

    def __str__(self):
        return self.suscripcion

    class meta:
        db_table= 'db_suscripcion'

class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=40)

    def __str__(self):
        return self.tipo
    class meta:
        db_table= 'db_tipo_producto'

class Usuario(models.Model):
    rut=models.IntegerField(null=False, primary_key=True)
    nombre=models.CharField(max_length=40)
    apellido=models.CharField(max_length=40)
    contraseña=models.CharField(max_length=20)
    comuna=models.CharField(max_length=30)
    direccion=models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class meta:
        db_table= 'db_usuario'

class Items_Carrito(models.Model):
    id_carro=models.AutoField(null=False, primary_key=True)
    nombre_producto= models.CharField(max_length=40)
    precio_producto= models.IntegerField()
    cantidad= models.IntegerField()
    imagen= models.ImageField(upload_to="items_carrito",null =True)

    def __str__(self):
        return self.nombre_producto
    def suma(self):
        resultado = self.precio_producto*self.cantidad
        return resultado
    

    class Meta: 
        db_table= 'db_items_carrito'

class Historial(models.Model):
    id_historial=models.AutoField(null=False, primary_key=True)
    nombre_historial= models.CharField(max_length=40)
    precio_historial= models.IntegerField()
    cantidad_historial= models.IntegerField()
    imagen_historial= models.ImageField(upload_to="historia",null =True)

    def __str__(self):
        return self.nombre_producto
    def suma(self):
        resultado = self.precio_historial*self.cantidad_historial
        return resultado


    class Meta: 
        db_table= 'db_Historial'