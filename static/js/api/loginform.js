$(document).ready(function(){
    $token = '';
    $('form').on('submit', function(){
        $.ajax({
            data: {
                name: $('#username').val(),
                password: $('#password').val()
            },
            type: 'POST',
            url: '/api/login'
        })
        .done(function(data){
            if(data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else{
                $('#errorAlert').hide();
                $('#successAlert').show();
                $token = data.token;
            }
        })
        event.preventDefault();
    });
    $('#view_companies').on('click', function(){
        $.ajax({
            type: 'GET',
            url: '/api/view_companies',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('x-access-token', $token);
            }
        })
        .done(function(data){
            $("#companies_selector").html("<select id='companies_lst' multiple></select>");
            $.each(data.companies, function(index, value){
                var o = new Option(value.name, value.id);
                $(o).html(value.name);
                $('#companies_lst').append(o);
            })

        })
    });

    $('#view_subcontractors').on('click', function(){
        $.ajax({
            type: 'GET',
            url: '/api/view_subcontractors',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('x-access-token', $token);
            }
        })
        .done(function(data){
            $.each(data.subcontractors, function(index, value){
                $('#successAlert').append('<br>' + value.code + '\t' + value.name + '\t' + value.address)
            })

        })
    });

});