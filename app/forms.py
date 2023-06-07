from dataclasses import field
from operator import imod
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Creamos un template para el formulario
class ProductoForm(ModelForm):
    
    nombre = forms.CharField(min_length=10,max_length=20)
    precio = forms.IntegerField(min_value=400)
    stock = forms.IntegerField(min_value=1)
    codigo = forms.IntegerField(min_value=1)
    cantidad = forms.IntegerField(min_value=1)
    class Meta:
        model= Producto
        fields=['codigo','nombre','raza','stock','descripcion','precio','cantidad','tipo','imagen']

        #widgets = {
        #    'fecha_ingreso' : forms.SelectDateWidget(years=range(2020,2023))
        #}

class UsuarioForm(ModelForm):
    
    class Meta:
        model= Usuario
        fields=['rut','nombre','apellido','contraseña','comuna','direccion','tipo']

        #widgets = {
        #    'fecha_ingreso' : forms.SelectDateWidget(years=range(2020,2023))
        #}

class RegistroUsuarioForm(UserCreationForm):
    
	class Meta: 
            model = User
            fields = ['username','first_name','last_name','email','password1','password2']