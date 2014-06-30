from django import forms
from viveres.models import TipoProducto
from viveres.models import Proveedor
from django.forms.fields import  ChoiceField,Select

TP_CHOICES = []
tp_all = TipoProducto.objects.all()
for tipo in tp_all:
    nuevo = (tipo.pk,tipo.nombre)
    TP_CHOICES.append(nuevo)
TP_CHOICES = tuple(TP_CHOICES)

class TProductoForm(forms.Form):
    tipo = ChoiceField(widget=Select, choices=TP_CHOICES,label='Tipo producto')
    #Select
    #tipo = forms.ModelChoiceField(queryset=TipoProducto.objects.all(),label='Tipo producto',attrs={'id': 'b_tproducto',})
     
class ProveedorFormu(forms.Form):
    tipo = forms.ModelChoiceField(queryset=Proveedor.objects.all(),label='Proveedor')
