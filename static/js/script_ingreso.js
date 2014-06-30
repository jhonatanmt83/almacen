$(function(){
    // Dialog2
    $('#agregar_dialog').dialog({
        autoOpen: false,
        width: 500,
        modal : true,
        buttons: {
            "Agregar": function() {
                var tp=$('#a_tproducto').val();
                var np=$('#a_nproducto').val();
                var cp=$('#a_cproducto').val();
                var pp=$('#a_pproducto').val();
                var tcp=$('#a_tcproducto').val();
                //var new_np = np.value.split(" ").join("_");
                var new_np = np.replace(/\s/g,"_");
                np = new_np;
                //alert(new_np);

                if (tp!='' && np!='' && cp!='' && pp!=''){
                    $.getJSON('/control/agregar/'+ cp+'/'+np+'/'+tp+'/'+pp+'/'+tcp,
                        function(data){
                            var resultado='';
                            var codigo = '';
                            $.each(data, function(index, resu){
                                resultado=resu['resultado'];
                                codigo=resu['codigo'];
                                tc=resu['tc'];
                                p=resu['p'];
                                nombre=resu['nombre'];
                                });
                            if (resultado=='agregado'){
                                $('#n_producto').val(nombre);
                                $('#id_producto').val(codigo);
                                $('#i_tipocantidad').val(tc);
                                $('#i_proveedor').val(p);
                                $('#agregar_dialog').dialog('close');
                                $('#buscar_dialog').dialog('close');
                            }
                            else if(resultado=='error1'){
                                alert('Ya existe un producto con el codigo '+codigo);
                            }
                            else{
                                alert('Error al agregar');
                            }
                        });
                     }
                else{
                    alert('Los campos son requeridos');
                }

                //$( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        }
    });
    // Dialog usar todo
    $('#usar_todo_dialog').dialog({
        autoOpen: false,
        width: 500,
        modal : true,
        buttons: {
            "Agregar": function() {
                var tp=$('#a_tproducto').val();
                var np=$('#a_nproducto').val();
                var cp=$('#a_cproducto').val();
                var pp=$('#a_pproducto').val();
                var tcp=$('#a_tcproducto').val();
                //var new_np = np.value.split(" ").join("_");
                var new_np = np.replace(/\s/g,"_");
                np = new_np;
                //alert(new_np);

                if (tp!='' && np!='' && cp!='' && pp!=''){
                    $.getJSON('/control/agregar/'+ cp+'/'+np+'/'+tp+'/'+pp+'/'+tcp,
                        function(data){
                            var resultado='';
                            var codigo = '';
                            $.each(data, function(index, resu){
                                resultado=resu['resultado'];
                                codigo=resu['codigo'];
                                tc=resu['tc'];
                                p=resu['p'];
                                nombre=resu['nombre'];
                                });
                            if (resultado=='agregado'){
                                $('#n_producto').val(nombre);
                                $('#id_producto').val(codigo);
                                $('#i_tipocantidad').val(tc);
                                $('#i_proveedor').val(p);
                                $('#agregar_dialog').dialog('close');
                                $('#buscar_dialog').dialog('close');
                            }
                            else if(resultado=='error1'){
                                alert('Ya existe un producto con el codigo '+codigo);
                            }
                            else{
                                alert('Error al agregar');
                            }
                        });
                     }
                else{
                    alert('Los campos son requeridos');
                    $( this ).dialog( "close" );
                }

                //$( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        }
    });
    $('#agregar_link').click(function(){
        $('#agregar_dialog').dialog('open');
        return false;
    });
    $('#usar_todo').click(function(){
        $('#usar_todo_dialog').dialog('open');
        return false;
    });
});

$("#formu_ingreso").submit( function () {
    $('#i_tipocantidad').removeAttr('disabled');
    $('#i_proveedor').removeAttr('disabled');
    return true;

});

$('#precio_unitario').keyup( function() {
    var cantidad = $('#i_cantidad').val();
    var total=parseInt(cantidad)*parseFloat($('#precio_unitario').val());
    var cadenita = total.toString();
    var pos = cadenita.indexOf('.');
    if (pos != -1){
        cadenita = cadenita.substr(0,pos+3);
    }
    if (isNaN(total)){
        $('#precio_total').val('');
    }
    else{
        $('#precio_total').val(cadenita);
    }

});



$("#usar_todo_check").click(function() {
    if($("#usar_todo_check:checked").val()=='yes'){
        $('#usar_todo_option').show();
    }else{
        $('#usar_todo_option').hide();
    }
});
