$(document).ready( function() {
    $("#password_reset_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            email: {
                required: true,
                email: true,
            },
        },
    });
});
