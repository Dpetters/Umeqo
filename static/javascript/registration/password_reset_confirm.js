/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
    
    password_reset_form_validator = $("#password_reset_confirm_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
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
                equalTo: "The passwords you entered don't match."
            }
        }
    });
});
