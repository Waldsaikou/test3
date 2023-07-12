import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from app.models import Historial
from django.db.models import Max
from .models import Seguimiento

from app.forms import ProductoForm
from app.forms import RegistroUsuarioForm
from .models import *
from .forms import *


# Create your views here.

#Funcion validar grupo
def grupo_requerido(nombre_grupo):
    def decorator(viwe_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(requests, *arg, **kwargs):
            return viwe_fuc(requests, *arg, **kwargs)
        return wrapper
    return decorator

#@grupo_requerido('vendedor')
#@grupo_requerido('cliente')
#@grupo_requerido('administrador')

#Seccion agregar
@grupo_requerido('vendedor')
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
@grupo_requerido('vendedor')
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
@grupo_requerido('vendedor')
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
@login_required
@permission_required('app.delete_historia')
def eliminarUsuario (request, historia):
    historia = historia.objects.get(historia=historia)
    historia.delete()

    return redirect(to="listarUsuario")
    
#SECCION LISTAR
@login_required
@grupo_requerido('vendedor')
@grupo_requerido('cliente')
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
    total = 0
    descuento = total * 0.05
    total_con_descuento = total - descuento
    for producto in carrito:
        total += (producto.precio_producto * producto.cantidad) - descuento
    # Obtener la última compra realizada
    ultima_compra = Historial.objects.latest('id_historial')
    if request.method == 'POST':
        for producto in carrito_items:
            # Restar la cantidad del producto del stock
            producto_obj = Producto.objects.get(codigo=producto.codigo_producto)
            producto_obj.stock -= producto.cantidad
            producto_obj.save()

        carrito_items.delete()
        return redirect('tienda')

    suscripcion_usuario = Suscripcion.objects.filter(usuario=request.user.username, suscripcion=True).first()
    if suscripcion_usuario:
        descuento = total * 0.05
        total_con_descuento = total - descuento
        mostrar_total_con_descuento = True
        ultima_compra.total = total
        ultima_compra.total_con_descuento = total_con_descuento
    else:
        total_con_descuento = total
        mostrar_total_con_descuento = False
        ultima_compra.total = total_con_descuento
        ultima_compra.total_con_descuento = total_con_descuento

    datosC = {
        'listaCarrito': carrito,
        'total': total,
        'total_con_descuento': total_con_descuento,
        'mostrar_total_con_descuento': mostrar_total_con_descuento,
        'ultima_compra': ultima_compra
    }

    if request.method == 'POST':
        historial = Historial()
        historial.nombre_historial = request.POST.get('nombre_producto')
        historial.precio_historial = request.POST.get('precio_producto')
        historial.imagen_historial = request.POST.get('imagen')
        historial.cantidad_historial = request.POST.get('cantidad')
        historial.usuario = request.user
        historial.save()

        

    return render(request, 'app/carro.html', datosC)

from django.shortcuts import redirect




@login_required
def eliminarCarro (request, id_carro):
    carro = Items_Carrito.objects.get(id_carro=id_carro)
    carro.delete()
    return redirect(to="carro")

def cart(request):
    response = requests.get('https://mindicador.cl/api/dolar')
    moneda = response.json()
    valor_dolar = moneda['serie'][0]['valor']
    total_carrito = {{ total }} 
    valor = total_carrito/valor_dolar 
    valor = round(valor, 2) 
    data = {
        'valor' : valor
    }  

    return render(request, 'app/carro.html', data)

    
@login_required
@grupo_requerido('vendedor')
@grupo_requerido('cliente')
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


from django.contrib import messages
from django.shortcuts import redirect
@login_required
def historia(request):
    historialAll = Historial.objects.all()
    datosH = {
        'listaHistorial': historialAll
    }
    
    if request.method == 'POST' and 'limpiar' in request.POST:
        # Eliminar todos los registros del historial
        Historial.objects.all().delete()
        
        # Mostrar un mensaje de éxito
        messages.success(request, 'El historial se ha limpiado correctamente.')
        
        # Redirigir a la misma página
        return redirect('historia')
    if request.method == 'POST':
        historial.usuario = request.user
        historial.save()

    return render(request, 'app/historia.html', datosH)
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
    suscripcionAll = Suscripcion.objects.all()
    datos = {
        'listasus': suscripcionAll
    }
    if request.method == 'POST':
        suscripcion = Suscripcion()
        suscripcion.suscripcion = request.POST.get('suscripcion')
        suscripcion.usuario = request.POST.get('usuario')

        # Verificar si el usuario está suscrito y aplicar descuento del 5%
        if suscripcion.suscripcion == 'True':
            total = 0  # Precio original del producto (ejemplo)
            descuento = total* 0.05
            precio_con_descuento = total - descuento
            suscripcion.precio_con_descuento = precio_con_descuento

        suscripcion.save()

    return render(request, 'app/suscripcion.html', datos)

@permission_required('app.delete_suscripcion')
def eliminarSuscripcion (request, id_suscripcion):
    suscripcion = Suscripcion.objects.get(id_suscripcion=id_suscripcion)
    suscripcion.delete()

    return redirect(to="suscripcion")

#Seccion listar

from django.shortcuts import get_object_or_404
from django.contrib import messages
@login_required
def tienda(request):
    response = requests.get('https://mindicador.cl/api/dolar/10-07-2023').json()
    json = response['serie']
    productosAll = Producto.objects.all()
    datos = {
        'listaProductos': productosAll,
        'listaRick': json
    }

    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        cantidad = int(request.POST.get('cantidad'))
        imagen = request.POST.get('imagen')

        # Obtener el producto y verificar el stock
        producto = get_object_or_404(Producto, nombre=nombre_producto)
        if cantidad > producto.stock:
            messages.error(request, 'No hay suficiente stock disponible.')
        else:
            # Restar la cantidad comprada al stock del producto
            producto.stock -= cantidad
            producto.save()

            # Guardar el producto en el carrito
            carrito = Items_Carrito(
                nombre_producto=nombre_producto,
                precio_producto=precio_producto,
                cantidad=cantidad,
                imagen=imagen
            )
            carrito.save()
            mensaje = 'El producto se ha agregado al carrito.'
            mensaje_js = f"mostrarMensaje('Éxito', '{mensaje}', 'success');"
            messages.success(request, mensaje_js)
    

    return render(request, 'app/tienda.html', datos)
def mostrarMensaje(request, mensaje, tipo):
    messages.add_message(request, tipo, mensaje)

from django.shortcuts import get_object_or_404
@login_required
def tienda(request):
    response = requests.get('https://mindicador.cl/api/dolar/14-06-2023').json()
    json = response['serie']
    productosAll = Producto.objects.all()
    datos = {
        'listaProductos': productosAll,
        'listaRick': json
    }

    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        cantidad = int(request.POST.get('cantidad'))
        imagen = request.POST.get('imagen')

        # Restar la cantidad comprada al stock del producto
        producto = get_object_or_404(Producto, nombre=nombre_producto)
        producto.stock -= cantidad
        producto.save()

        # Guardar el producto en el carrito
        carrito = Items_Carrito(
            nombre_producto=nombre_producto,
            precio_producto=precio_producto,
            cantidad=cantidad,
            imagen=imagen
        )
        carrito.save()

    return render(request, 'app/tienda.html', datos)

@login_required
@grupo_requerido('vendedor')

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


from .models import Items_Carrito, Producto

def historial(request):
    historial_items = Items_Carrito.objects.filter(historial=True)
    datos = []

    for item in historial_items:
        producto = Producto.objects.get(codigo=item.codigo_producto)
        datos.append({
            'nombre_producto': producto.nombre,
            'precio_producto': producto.precio,
            'cantidad': item.cantidad,
            # Agrega otros campos relevantes del producto que deseas mostrar en el historial
        })

    return render(request, 'app/historial.html', {'historial_items': datos})

from .models import Items_Carrito, Historial, Suscripcion

def carro(request):
    carrito_items = Items_Carrito.objects.all()
    total = 0
    descuento = total * 0.05
    total_con_descuento = total - descuento

    for producto in carrito_items:
        total += ((producto.precio_producto * producto.cantidad) - descuento)

    suscripcion_usuario = Suscripcion.objects.filter(usuario=request.user.username, suscripcion=True).first()
    if suscripcion_usuario:
        descuento = total * 0.05
        total_con_descuento = total - descuento
        mostrar_total_con_descuento = True
    else:
        total_con_descuento = total
        mostrar_total_con_descuento = False

    if request.method == 'POST':
        for producto in carrito_items:
            historial = Historial()
            historial.nombre_historial = producto.nombre_producto
            historial.precio_historial = producto.precio_producto
            historial.imagen_historial = producto.imagen
            historial.cantidad_historial = producto.cantidad
            historial.save()

        carrito_items.delete()  # Elimina los productos del carrito después de guardarlos como historial

    datosC = {
        'listaCarrito': carrito_items,
        'total': total,
        'total_con_descuento': total_con_descuento,
        'mostrar_total_con_descuento': mostrar_total_con_descuento
    }

    return render(request, 'app/carro.html', datosC)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Seguimiento

@login_required
def seguimiento_compra(request):
    # Obtener el seguimiento de compra del usuario actual
    seguimiento = Seguimiento.objects.filter(usuario=request.user).first()

    if seguimiento:
        codigo_seguimiento = seguimiento.codigo_compra
        hora_compra = seguimiento.fecha_compra.strftime("%Y-%m-%d %H:%M:%S")
        nombre_comprador = f"{request.user.first_name} {request.user.last_name}"
        id_seguimiento = seguimiento.id

        datos = {
            'codigo_seguimiento': codigo_seguimiento,
            'hora_compra': hora_compra,
            'nombre_comprador': nombre_comprador,
            'id_seguimiento': id_seguimiento
        }
        return render(request, 'app/seguimiento.html', datos)
    else:
        # Si no hay seguimiento de compra, mostrar un mensaje o redirigir a otra página
        return render(request, 'app/seguimiento_vacio.html')



