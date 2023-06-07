import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

from app.forms import ProductoForm
from app.forms import RegistroUsuarioForm
from .models import *
from .forms import *


# Create your views here.

#Seccion agregar
@login_required
@permission_required('app.add_producto')
def agregarProducto(request):
    datos ={
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto guardado correctamente!')

    return render(request, 'app/productos/agregarProducto.html',datos)

@login_required
@permission_required('app.add_usuario')
def agregarUsuario(request):
    datosU ={
        'form1' : UsuarioForm()
    }

    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datosU['Mensaje']= 'Usuario guardado correctamente'

    return render(request, 'app/usuarios/agregarUsuario.html',datosU)          

#SECCION MODIFICAR
@login_required
@permission_required('app.change_producto')
def modificarProducto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    datos ={
        'form' : ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES,instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto modificado correctamente!')
            datos['form'] = formulario

    return render(request, 'app/productos/modificarProducto.html',datos)    

@login_required
@permission_required('app.delete_producto')
def eliminarProducto (request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    producto.delete()

    return redirect(to="listarProductos")

@login_required
@permission_required('app.change_usuario')
def modificarUsuario(request, rut):
    usuario = Usuario.objects.get(rut=rut)
    datosU ={
        'form1' : UsuarioForm(instance=usuario)
    }

    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, files=request.FILES,instance=usuario)
        if formulario.is_valid():
            formulario.save()
            datosU['Mensaje']= 'Usuario modificado correctamente'
            datosU['form1'] = formulario

    return render(request, 'app/usuarios/modificarUsuario.html',datosU)    

@login_required
@permission_required('app.delete_usuario')
def eliminarUsuario (request, rut):
    usuario = Usuario.objects.get(rut=rut)
    usuario.delete()

    return redirect(to="listarUsuario")
#SECCION LISTAR
@login_required
@permission_required('app.view_producto')
def listarProductos(request):
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll
    }
    return render(request, 'app/productos/listarProductos.html', datos)

@login_required
@permission_required('app.view_usuario')
def listarUsuario(request):
    usuarioAll= Usuario.objects.all()
    datosU ={
        'listaUsuario':usuarioAll
    }
    return render(request, 'app/usuarios/listarUsuario.html',datosU)

def listarUsuarioApi(request):
    response = requests.get('http://127.0.0.1:8000/api/usuario/').json()
    usuarioAll= Usuario.objects.all()
    datosU ={
        'listaUsuario':usuarioAll,
        'listaApi':response
    }
    return render(request, 'app/usuarios/listarUsuarioApi.html',datosU)


def index(request):
    return render(request, 'app/index.html')

@login_required
@permission_required('app.view_items_carrito')
def carro(request):
    carrito = Items_Carrito.objects.all()
    datosC ={
        'listaCarrito':carrito
    }
    if request.method == 'POST':
        historial = Historial()
        historial.nombre_historial = request.POST.get('nombre_producto')
        historial.precio_historial = request.POST.get('precio_producto')
        historial.imagen_historial = request.POST.get('imagen')
        historial.cantidad_historial= request.POST.get('cantidad')
        historial.save()
    return render(request, 'app/carro.html',datosC)

@login_required
def eliminarCarro (request, id_carro):
    carro = Items_Carrito.objects.get(id_carro=id_carro)
    carro.delete()
    return redirect(to="carro")
    
@login_required
def animalespequeños(request):
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll
    }
    if request.method == 'POST':
        carrito = Items_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.cantidad = request.POST.get('cantidad')
        carrito.imagen = request.POST.get('imagen')
        carrito.save()
    return render(request, 'app/animalespequeños.html',datos)

@login_required
def cuenta(request):
    usuarioAll= Usuario.objects.all()
    datosU ={
        'listaUsuario':usuarioAll
    }
    return render(request, 'app/cuenta.html',datosU)

@login_required
def datos(request):
    return render(request, 'app/datos.html')

def formularioCrearCuenta(request):
    return render(request, 'app/formularioCrearCuenta.html')

@login_required
def fundacion(request):
    return render(request, 'app/fundacion.html')

@login_required
def gatos(request):
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll
    }
    if request.method == 'POST':
        carrito = Items_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.cantidad = request.POST.get('cantidad')
        carrito.imagen = request.POST.get('imagen')
        carrito.save()
    return render(request, 'app/gatos.html',datos)

@login_required
def historia(request):
    historialAll= Historial.objects.all()
    datosH={
        'listaHistorial':historialAll
    }
    return render(request, 'app/historia.html',datosH)

@login_required
def inicioSexionIni(request):
    return render(request, 'app/inicioSexionIni.html')

@login_required
def perros(request):
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll
    }
    if request.method == 'POST':
        carrito = Items_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.cantidad = request.POST.get('cantidad')
        carrito.imagen = request.POST.get('imagen')
        carrito.save()
    return render(request, 'app/perros.html', datos)

@login_required
def seguimiento(request):
    return render(request, 'app/seguimiento.html')

@login_required
def suscripcion(request):
    suscripcionAll=Suscripcion.objects.all()
    datos={
        'listasus':suscripcionAll
    }
    if request.method == 'POST':
        suscripcion = Suscripcion()
        suscripcion.suscripcion = request.POST.get('suscripcion')
        suscripcion.usuario = request.POST.get('usuario')
        suscripcion.save()
    return render(request, 'app/suscripcion.html',datos)

@permission_required('app.delete_suscripcion')
def eliminarSuscripcion (request, id_suscripcion):
    suscripcion = Suscripcion.objects.get(id_suscripcion=id_suscripcion)
    suscripcion.delete()

    return redirect(to="suscripcion")

#Seccion listar
@login_required
def tienda(request):
    response = requests.get('https://mindicador.cl/api/uf/11-07-2022').json()
    json=response['serie']
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll,
        'listaRick': json
    }
    if request.method == 'POST':
        carrito = Items_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.cantidad = request.POST.get('cantidad')
        carrito.imagen = request.POST.get('imagen')
        carrito.save()
    return render(request, 'app/tienda.html',datos)

@login_required
def tiendaApi(request):
    response = requests.get('http://127.0.0.1:8000/api/producto/').json()
    productosAll= Producto.objects.all()
    datos ={
        'listaProductos':productosAll,
        'listaJson': response
    }
    if request.method == 'POST':
        carrito = Items_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.imagen = request.POST.get('imagen')
        carrito.save()
    return render(request, 'app/tiendaApi.html',datos)


def registro(request):
    datos = {
        'form' : RegistroUsuarioForm()
    }
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request,'Registrado correctamente!')
            return redirect(to="cuenta")
        datos["form"] = formulario
    return render(request, 'registration/registro.html',datos)


