$(document).ready( function() {
    $("#choose_new_password_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            new_password1: {
                required: true,
                minlength: PASSWORD_MIN_LENGTH,
            },
            new_password2:{
                required: true,
                equalTo: '#id_new_password1'
            },
        },
        messages:{
            new_password2:{
                equalTo: PASSWORDS_DONT_MATCH_MESSAGE
            }
        }
    });
});
