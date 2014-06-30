# -*- coding: utf-8 -*-
from django.db import models
import os
import datetime
from django import forms
from django.forms import ModelForm,Select,TextInput,ImageField
from django.contrib.auth.models import User

# Create your models here.
class formingreso(forms.Form):
    usuarioform = forms.CharField(label='Usuario')
    passform = forms.CharField(label='Clave',widget=forms.PasswordInput(render_value=False))

class Estcivil(models.Model):
    codigo = models.CharField(max_length=2, verbose_name='codigo', primary_key=True)
    nombre = models.CharField(max_length=12, verbose_name='estado:')

    def __unicode__(self):
        return self.nombre

class EstcivilForm(ModelForm):
    class Meta:
        model = Estcivil

#~ class Sucursal(models.Model):
    #~ nombre = models.CharField(max_length=12, verbose_name='Nombre')
    #~ direccion = models.CharField(max_length=50, verbose_name='Direccion')
    #~ def __unicode__(self):
        #~ return self.nombre
#~
#~ class SucursalForm(ModelForm):
    #~ class Meta:
        #~ model = Sucursal

class Cargo(models.Model):
    nombre = models.CharField(max_length=15, verbose_name='Cargo')

    def __unicode__(self):
        return self.nombre

class CargoForm(ModelForm):
    class Meta:
        model = Cargo

class Persona(models.Model):
    dni = models.CharField(max_length=8, verbose_name='Nro. del documento de identidad', primary_key=True)
    usuario = models.ForeignKey(User,verbose_name='Usuario')
    cargo = models.ForeignKey(Cargo ,verbose_name='Cargo')
    genero = models.CharField(max_length=1, choices=(('M','Masculino'),('F','Femenino')))
    estadocivil = models.ForeignKey(Estcivil ,verbose_name='Estado civil')
    direccion = models.CharField(max_length=50 ,verbose_name='Direccion')
    celular = models.CharField(max_length=9,verbose_name='Celular o Telefono')
    #sucursal = models.ForeignKey(Sucursal ,verbose_name='Sucursal')

    def __unicode__(self):
        cadena=str(self.usuario.first_name)+" "+str(self.usuario.last_name)
        return cadena


class PersonaForm(ModelForm):
    class Meta:
        model = Persona

#Para el proveedor
#~ class TipoProveedor(models.Model):
    #~ nombre = models.CharField(max_length=15, verbose_name='Tipo:')
    #~
    #~ def __unicode__(self):
        #~ return self.nombre
#~
#~ class TipoProveedorForm(ModelForm):
    #~ class Meta:
        #~ model = TipoProveedor

#entidad que registra
class Proveedor(models.Model):
    nombre = models.CharField(max_length=15, verbose_name='Nombre')
    direccion = models.CharField(max_length=50, verbose_name='Direccion')
    celular = models.CharField(max_length=15, verbose_name='Celular/Telefono')
    email = models.EmailField(max_length=75,verbose_name='E-mail')
    #tipoproveedor = models.ForeignKey(TipoProveedor ,verbose_name='Tipo Proveedor')

    def __unicode__(self):
        return self.nombre

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        widgets = {
            'nombre': TextInput(attrs={'id':'a_nproveedor'}),
            'direccion': TextInput(attrs={'id':'a_dproveedor'}),
            'celular': TextInput(attrs={'id':'a_cproveedor'}),
            'email': TextInput(attrs={'id':'a_eproveedor'}),
         }


#Para el producto
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=15, verbose_name='Tipo Producto')

    def __unicode__(self):
        return self.nombre

class TipoProductoForm(ModelForm):
    class Meta:
        model = TipoProducto


class TipoCantidad(models.Model):
    abreviacion = models.CharField(max_length=3, verbose_name='Abreviacion')
    nombre = models.CharField(max_length=15)

    def __unicode__(self):
        return self.nombre

class TipoCantidadForm(ModelForm):
    class Meta:
        model = TipoCantidad

class Producto(models.Model):
    codigo = models.CharField(max_length=7, verbose_name='Codigo',primary_key=True)
    nombre = models.CharField(max_length=15, verbose_name='Nombre')
    tipo = models.ForeignKey(TipoProducto,verbose_name='Tipo')
    proveedor = models.ForeignKey(Proveedor,verbose_name='Proveedor')
    cantidad = models.CharField(max_length=20, verbose_name='Cantidad')
    tipo_cantidad = models.ForeignKey(TipoCantidad,verbose_name='Unidad')
    #peso = models.CharField(max_length=20, verbose_name='Peso')

    def __unicode__(self):
        return self.nombre

class ProductoForm(ModelForm):
    class Meta:
        model = Producto

class BusquedaForm(ModelForm):
     class Meta:
         model = Producto
         exclude = ('proveedor','cantidad','tipo_cantidad')
         widgets = {
            'tipo': Select(attrs={'id':'b_tproducto'}),
            'codigo': TextInput(attrs={'id':'b_cproducto'}),
            'nombre': TextInput(attrs={'id':'b_nproducto'}),
         }
class NuevoProductoForm(ModelForm):
     class Meta:
         model = Producto
         exclude = ('cantidad')
         widgets = {
            'tipo': Select(attrs={'id':'a_tproducto'}),
            'proveedor': Select(attrs={'id':'a_pproducto'}),
            'codigo': TextInput(attrs={'id':'a_cproducto'}),
            'nombre': TextInput(attrs={'id':'a_nproducto'}),
            'tipo_cantidad': Select(attrs={'id':'a_tcproducto'}),
         }

#Transacciones
class Salida(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto ,verbose_name='Producto')
    persona = models.ForeignKey(Persona,verbose_name='Persona')
    cantidad = models.CharField(max_length=15, verbose_name='Cantidad')
    tipo_cantidad = models.ForeignKey(TipoCantidad,verbose_name='Unidad')
    stock_restante = models.CharField(max_length=15, verbose_name='Stock Restante')
    comida = models.CharField(max_length=1, choices=(('D','Desayuno'),('A','Almuerzo')),default='D')

    def __unicode__(self):
        return str(self.producto)

    def precio_unitario(self):
        ingresos = Ingreso.objects.filter(producto=self.producto,fecha__lt=self.fecha)
        ingresos = ingresos.order_by('-fecha')
        ingreso=ingresos[0]
        return ingreso.precio_unitario

    def precio_total(self):
        retornar=float(self.precio_unitario())*int(self.cantidad)
        return retornar

class SalidaForm(ModelForm):
    class Meta:
        model = Salida
        exclude = ('producto')
        widgets = {
            'stock_restante':TextInput(attrs={'id':'stock'}),
            'tipo_cantidad': Select(attrs={'id':'i_tipocantidad','disabled':'true;'}),
            'cantidad':TextInput(attrs={'id':'cantidad_sacada'}),
         }

class Ingreso(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto ,verbose_name='Producto')
    proveedor = models.ForeignKey(Proveedor,verbose_name='Proveedor')
    cantidad = models.CharField(max_length=15, verbose_name='Cantidad')
    tipo_cantidad = models.ForeignKey(TipoCantidad,verbose_name='Tipo')
    guia_remision = models.CharField(max_length=12, verbose_name='Guia de Remision')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Precio unitario S/.')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Precio total S/.')

    def __unicode__(self):
        return str(self.producto)

class IngresoForm(ModelForm):
    class Meta:
        model = Ingreso
        exclude = ('producto',)
        widgets = {
            'tipo_cantidad': Select(attrs={'id':'i_tipocantidad','disabled':'true;'}),
            'proveedor': Select(attrs={'id':'i_proveedor','disabled':'true;'}),
            'precio_unitario': TextInput(attrs={'id':'precio_unitario'}),
            'precio_total': TextInput(attrs={'id':'precio_total'}),
            'cantidad': TextInput(attrs={'id':'i_cantidad'}),
        }

#~
#~ class Stock(models.Model):
    #~ fecha = models.DateTimeField(auto_now_add=False)
    #~ producto = models.ForeignKey(Producto ,verbose_name='Producto')
    #~ cantidad = models.CharField(max_length=15, verbose_name='Cantidad')
    #~ salida = models.ForeignKey(Salida,verbose_name='Salida')
    #~
    #~ def __unicode__(self):
        #~ return self.nombre
#~
#~ class StockForm(ModelForm):
    #~ class Meta:
        #~ model = Stock




