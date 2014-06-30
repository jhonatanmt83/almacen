# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import inlineformset_factory

from viveres.models import formingreso
from viveres.models import Estcivil,EstcivilForm
from viveres.models import Cargo,CargoForm
from viveres.models import Persona,PersonaForm
from viveres.models import Proveedor,ProveedorForm
from viveres.models import TipoProducto,TipoProductoForm
from viveres.models import TipoCantidad,TipoCantidadForm
from viveres.models import Producto,ProductoForm
from viveres.models import Salida,SalidaForm
from viveres.models import Ingreso,IngresoForm
from viveres.models import NuevoProductoForm,BusquedaForm

import datetime
import json
from django.db.models import Q
from datetime import datetime

def ingreso(request):
    if request.method == 'POST':
        formu = formingreso(request.POST)
        usuariologin = request.POST['usuarioform']
        passlogin = request.POST['passform']
        acceso = authenticate(username=usuariologin,password=passlogin)
        if acceso is not None:
            if acceso.is_active:
                login(request,acceso)
                return HttpResponseRedirect('/control/')
            else:
                return render_to_response('registration/noactivo.html')
        else:
            return render_to_response('registration/nousuario.html')
    else:
        formu = formingreso()
    return render_to_response('registration/login.html',{'formu':formu},context_instance=RequestContext(request))

def salida(request):
    logout(request)
    return render_to_response('registration/logout.html')

@login_required
def control(request):
    return render_to_response('control.html',{},context_instance=RequestContext(request))

@login_required
def controlingreso(request):
    bform = BusquedaForm
    npform = NuevoProductoForm
    datos={}
    datos['producto']=''
    mensaje ={}
    if request.POST:
        try:
            formulario = IngresoForm(request.POST)
            producto=Producto.objects.get(pk=request.POST['producto'])
            datos['producto'] = request.POST['producto']
            datos['nombre_producto'] = producto.nombre
            if request.POST['usar_todo']=='yes': datos['option_usar_todo']=request.POST['option']
            new_form = formulario.save(commit=False)
            new_form.producto=producto
            new_form.save()
            if request.POST['usar_todo']=='yes': datos['option_usar_todo']=request.POST['option']
            if formulario.is_valid():
                grabado=formulario.save()
                #establecer nuevo stock
                producto.cantidad = str(int(producto.cantidad)+int(request.POST['cantidad']))
                producto.save()
                if request.POST['usar_todo']=='yes':
                    stock_restante_s=str(int(producto.cantidad)-int(request.POST['cantidad']))
                    cantidad_s=request.POST['cantidad']
                    tipo_cantidad_s=TipoCantidad.objects.get(pk=request.POST['tipo_cantidad'])
                    comida_s=request.POST['option']
                    persona_s=Persona.objects.filter(usuario=request.user)[0]
                    salida = Salida(producto=producto,persona=persona_s,cantidad=cantidad_s,tipo_cantidad=tipo_cantidad_s,stock_restante=stock_restante_s,comida=comida_s)
                    salida.save()
                    producto.cantidad = str(int(producto.cantidad)-int(request.POST['cantidad']))
                    producto.save()
                formulario = IngresoForm
                #establecer campos vacios
                datos['producto'] = ''
                mensaje['titulo']='Informacion'
                mensaje['contenido']='Datos de Ingreso Agregado.'
            else:
                return render_to_response('control_ingreso.html',{'formulario':formulario,'bform':bform,'npform':npform,'datos':datos,'mensaje':mensaje},context_instance=RequestContext(request))
        except:
            formulario = IngresoForm(request.POST)
    else:
        formulario = IngresoForm
    return render_to_response('control_ingreso.html',{'formulario':formulario,'bform':bform,'npform':npform,'datos':datos,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required
def controlsalida(request):
    bform = BusquedaForm
    datos={}
    datos['producto'] = ''
    datos['persona'] = Persona.objects.filter(usuario=request.user)[0].dni
    mensaje ={}
    if request.POST:
        try:
            formulario = SalidaForm(request.POST)
            producto=Producto.objects.get(pk=request.POST['producto'])
            datos['producto']=request.POST['producto']
            datos['stock']=producto.cantidad
            new_form = formulario.save(commit=False)
            new_form.producto=producto
            new_form.save()
            if formulario.is_valid():
                grabado=formulario.save()
                #establecer nuevo stock
                producto.cantidad = str(int(producto.cantidad)-int(request.POST['cantidad']))
                producto.save()
                formulario = SalidaForm
                #establecer campos vacios
                datos['producto'] = ''
                #mensaje de agregado
                mensaje['titulo']='Informacion'
                mensaje['contenido']='Datos de Salida Agregado.'
            else:
                return render_to_response('control_salida.html',{'formulario':formulario,'bform':bform,'mensaje':mensaje,'datos':datos},context_instance=RequestContext(request))
        except:
            formulario = SalidaForm(request.POST)
    else:
        formulario = SalidaForm
    return render_to_response('control_salida.html',{'formulario':formulario,'bform':bform,'mensaje':mensaje,'datos':datos},context_instance=RequestContext(request))


@login_required
def busqueda(request,tipo_producto,nombre,codigo):
    """Devuelve las coincidencias de busqueda de acuerdo a los datos para el js"""
    resultado= []
    if tipo_producto != 'none':
        tproducto = TipoProducto.objects.get(pk=tipo_producto)
        resultado = Producto.objects.filter(tipo=tproducto)
    if nombre != 'none':
        resul2 = Producto.objects.filter(nombre__contains=nombre)
        for x in resul2:
            if not x in resultado:
                resultado.append(x)
    if codigo != 'none':
        resul2 = Producto.objects.filter(codigo__contains=codigo)
        for x in resul2:
            if not x in resultado:
                resultado.append(x)

    total = len(resultado)

    new_result=[]
    for producto in resultado:
        datos = {}
        datos['codigo'] = producto.codigo
        datos['nombre'] = producto.nombre
        datos['tipo'] = producto.tipo.nombre
        datos['proveedor_id'] = producto.proveedor.pk
        datos['tc_id'] = producto.tipo_cantidad.pk
        datos['stock']=producto.cantidad

        new_result.append(datos)

    return HttpResponse( json.dumps(new_result) )

@login_required
def agregar(request,codigo,nombre,tipo,proveedor,tcantidad):
    """Agrega nuevos productos"""
    sw = True
    #~ sw = False
    if not Producto.objects.filter(pk=codigo):
        try:
            tproducto = TipoProducto.objects.get(pk=tipo)
            pproducto = Proveedor.objects.get(pk=proveedor)
            cantidad = 0
            tipo_cantidad = TipoCantidad.objects.get(pk=tcantidad)
            nombre = nombre.replace("_"," ")
            new_product = Producto(codigo=codigo,nombre=nombre,tipo=tproducto,proveedor=pproducto,cantidad=cantidad,tipo_cantidad=tipo_cantidad)
            new_product.save()
            codigo = new_product.pk
            t_cantidad = new_product.tipo_cantidad.pk
            prove = new_product.proveedor.pk
        except:
            sw=False
    else:
        resultado=[{'resultado':'error1','codigo':codigo}]
        return HttpResponse( json.dumps(resultado) )
    if sw:
        resultado=[{'resultado':'agregado','codigo':codigo,'tc':t_cantidad,'p':prove,'nombre':nombre}]
    else:
        codigo = 0
        resultado=[{'resultado':'error','codigo':codigo}]

    return HttpResponse( json.dumps(resultado) )

@login_required
def encontrar_codigo(request,codigo):
    """Encuentra datos de los productos"""
    producto = Producto.objects.get(pk=codigo)
    resultado=[{'codigo':producto.pk,'proveedor':producto.proveedor.pk,'tc':producto.tipo_cantidad.pk}]

    return HttpResponse( json.dumps(resultado) )

def error404(request):
    return render_to_response('404.html',{})

@login_required
def proveedores(request):
    proveedores=Proveedor.objects.all()
    prove_form=ProveedorForm()
    return render_to_response('proveedores.html',{'proveedores':proveedores},context_instance=RequestContext(request))

@login_required
def agregar_nuevo(request,modelo):
    modelos = {'proveedor':{'model':ProveedorForm,'url':'/control/proveedores/'}}
    formulario = modelos[modelo]['model']
    if request.POST:
        formulario = formulario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(modelos[modelo]['url'])
            formulario = modelos[modelo]
        else:
            #formulario = formulario(request.POST)
            pass
    else:
        formulario = modelos[modelo]['model']
    return render_to_response('agregar.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required
def reporte(request):
    meses={'1':'Enero','2':'Febrero','3':'Marzo','4':'Abril','5':'Mayo','6':'Junio','7':'Julio','8':'Agosto','9':'Setiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
    reportes={}
    retornar = []
    mes=''
    tipo_reporte=''
    consulta=''
    id_mes = 1
    if request.POST:
        if request.POST['tipo_reporte']=='mes':
            mes = int(request.POST['mes'])
            anio = int(request.POST['anio'])
            mes_post = mes + 1
            fecha_inicio = datetime(anio,mes,1, 0, 00)
            if mes_post > 12:
                mes_post = 0
                anio = anio + 1
            fecha_fin = datetime(anio,mes_post,1, 0, 00)
            cad_fecha='/'+str(mes)+'/'+str(anio)
            salidas = Salida.objects.filter(fecha__gte = fecha_inicio,fecha__lt = fecha_fin)
            salidas = salidas.order_by('producto')
            products=[]
            for x in salidas:
                if not x.producto in products:
                    products.append(x.producto)
            new_salidas=[]
            for producto in products:
                dias_producto=[]
                total_a=0
                for dia in range(1,32):
                    fecha=str(dia)+cad_fecha
                    dia_salida = salidas.filter(fecha__day=dia,producto=producto)
                    if len(dia_salida)>0:
                        cantidad_t=0
                        total_t=0
                        unidad_t=''
                        for sali in dia_salida:
                            total_t += float(sali.precio_total())
                            cantidad_t += int(sali.cantidad)
                        total_a +=total_t
                        proveedor_t =producto.proveedor
                        unidad_t =producto.tipo_cantidad
                        dias_producto.append({'dia':fecha,'proveedor':proveedor_t,'cantidad':cantidad_t,'unidad':unidad_t,'total':total_t})
                new_salidas.append({'producto':producto,'dias':dias_producto,'total':total_a})
            mes=meses[str(mes)]
            id_mes = request.POST['mes']
            tipo_reporte='mes'
            return render_to_response('reporte.html',{'reporte':tipo_reporte,'productos':new_salidas,'mes':mes,'id_mes':id_mes},context_instance=RequestContext(request))
        elif request.POST['tipo_reporte']=='dia':
            fecha=request.POST['fecha']
            devolver_fecha=fecha
            dia,mes,anio=fecha.split('/')
            fecha_inicio = datetime(int(anio),int(mes),int(dia), 0, 00)
            fecha_fin = datetime(int(anio),int(mes),int(dia)+1, 0, 00)
            salidas = Salida.objects.filter(fecha__gte = fecha_inicio,fecha__lt = fecha_fin)
            desayunos = salidas.filter(comida = 'D')
            almuerzos = salidas.filter(comida = 'A')
            tipo_reporte='dia'
            return render_to_response('reporte.html',{'reporte':tipo_reporte,'desayunos':desayunos,'almuerzos':almuerzos,'fecha':devolver_fecha},context_instance=RequestContext(request))
    return render_to_response('reporte.html',{'reporte':tipo_reporte,'reportes':retornar,'mes':mes,'consulta':consulta,'id_mes':id_mes},context_instance=RequestContext(request))

def valido(diccio,valor):
    try:
        retornar = diccio[valor]
    except:
        retornar=''
    return retornar
