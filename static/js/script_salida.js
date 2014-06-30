

$('#cantidad_sacada').keyup( function() {
    var restante=parseInt(cantidad)-parseInt($('#cantidad_sacada').val());
    if (isNaN(restante)){
        $('#stock').val(cantidad);
    }
    else{
        $('#stock').val(restante);
    }

});

$("#formu_salida").submit( function () {
    if (parseInt($('#stock').val())<0){
        alert('Cantidad ingresada incorrecta');
        return false;
    }
    else{
        $('#i_tipocantidad').removeAttr('disabled');
        return true;
    }
});
