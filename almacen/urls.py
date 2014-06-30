# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','viveres.views.ingreso'),
    url(r'^login/$','viveres.views.ingreso'),
    url(r'^salir/$','viveres.views.salida'),
    url(r'^control/$','viveres.views.control'),
    url(r'^control/ingreso/$','viveres.views.controlingreso'),
    url(r'^control/salida/$','viveres.views.controlsalida'),
    url(r'^control/proveedores/$','viveres.views.proveedores'),
    url(r'^control/busqueda/(?P<tipo_producto>\w+)/(?P<nombre>\w+)/(?P<codigo>\w+)$','viveres.views.busqueda'),
    url(r'^control/agregar/(?P<codigo>\w+)/(?P<nombre>\w+)/(?P<tipo>\w+)/(?P<proveedor>\w+)/(?P<tcantidad>\w+)$','viveres.views.agregar'),
    #url(r'^control/agregar/proveedor/(?P<nombre>\w+)/(?P<direccion>\w+)/(?P<celular>\w+)/(?P<email\w+)$','viveres.views.agregar_proveedor'),
    url(r'^control/(?P<modelo>\w+)/agregar/$','viveres.views.agregar_nuevo'),
    url(r'^control/reporte/$','viveres.views.reporte'),
    # Examples:
    # url(r'^$', 'almacen.views.home', name='home'),
    # url(r'^almacen/', include('almacen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
            {'document_root':settings.MEDIA_ROOT,}
        ),
)

handler404 = 'viveres.views.error404'
