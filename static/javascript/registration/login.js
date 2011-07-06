$(document).ready(function() {
    var login_main_form_validator = $('#login_main_form').validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
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
                required: 'Enter your email.',
                email: 'Invalid email.'
            },
            password: 'Enter a password.',
        }
    });
    if (VALIDATE_ON_LOAD) {
        $('#login_main_form').valid();
    }
});
