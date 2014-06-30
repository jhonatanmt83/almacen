from django.contrib import admin
from viveres.models import Estcivil
from viveres.models import Cargo
from viveres.models import Persona
from viveres.models import Proveedor
from viveres.models import TipoProducto
from viveres.models import TipoCantidad
from viveres.models import Producto
from viveres.models import Salida
from viveres.models import Ingreso


admin.site.register(Estcivil)
admin.site.register(Cargo)
admin.site.register(Persona)
admin.site.register(Proveedor)
admin.site.register(TipoProducto)
admin.site.register(TipoCantidad)
admin.site.register(Producto)
admin.site.register(Salida)
admin.site.register(Ingreso)
