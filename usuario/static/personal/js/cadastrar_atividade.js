$(document).ready(function() {

    $('select').material_select();

    $('.datepicker').pickadate({
        selectMonths: true,
        selectYears: 20,
        today: 'Hoje',
        clear: 'Limpar',
        close: 'Ok',
        closeOnSelect: false
    });
});


