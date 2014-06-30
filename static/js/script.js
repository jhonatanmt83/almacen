function mostrar_resultados(data){
    $('#resu').empty(); //elimino el cotenido actual del tbody
    // agrego los tipos obtenidos por ajax
    var contador=0;
    $.each(data, function(index, producto){
        $('<tr onDblClick="encuentra_producto( '+producto['codigo'] +','+producto['tc_id']+','+producto['proveedor_id']+','+producto['stock']+',\''+producto['nombre']+'\')">'+
            '<td>' + producto['codigo'] + '</td>' +
            '<td>' + producto['nombre'] + '</td>' +
            '<td>' + producto['tipo'] + '</td>' +
            '</tr>').appendTo('#resu');
        contador++;
    });
    $('#total_resultados').empty();
    var cadena='<span>'+contador+' coincidencias</span>';
    $(cadena).appendTo('#total_resultados');

    $('#buscar_dialog').dialog('close');
    $('#buscar_dialog').dialog('open');
}


function encuentra_producto(cod_producto,tc,p,s,nombre){
    $('#id_producto').val(cod_producto);
    $('#i_tipocantidad').val(tc);
    $('#i_proveedor').val(p);
    $('#stock').val(s);
    $('#n_producto').val(nombre);
    $('#buscar_dialog').dialog('close');
    cantidad = parseInt(s);
}

function rellena_datos(cod_producto){
    $.getJSON('/control/rellena/'+ cod_producto,
           function(data){
               $.each(data, function(index, producto){
                    $('#id_producto').val(codigo);
                    $('#i_tipocantidad').val(tc);
                    $('#i_proveedor').val(poveedor);
               });
            });
}

$(function(){
    // Dialog
    $('#buscar_dialog').dialog({
        autoOpen: false,
        width: 500,
        modal : true,
    });
    $('#mensaje_dialog').dialog({
        autoOpen: true,
        width: 300,
        modal : true,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );
            }
        }
    });

    // Dialog Link
    $('#buscar_link').click(function(){
        $('#buscar_dialog').dialog('open');
        return false;
    });


    $('#busqueda_link').click(function(){
        var tp=$('#b_tproducto').val();
        var np=$('#b_nproducto').val();
        var cp=$('#b_cproducto').val();
        if (tp==''){tp='none';}
        if (np==''){np='none';}
        if (cp==''){cp='none';}
        $.getJSON('/control/busqueda/'+ tp+'/'+np+'/'+cp,
           function(data){ mostrar_resultados(data) });

        return false;
    });
});



