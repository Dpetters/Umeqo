$(document).ready( function() {
    $("#login_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            username: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
        },
        messages: {
            username: {
                required: EMAIL_REQUIRED_MESSAGE,
                email: INVALID_EMAIL_MESSAGE
            },
            password: PASSWORD_REQUIRED_MESSAGE
        }
    });
});