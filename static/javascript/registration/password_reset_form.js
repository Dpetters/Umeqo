/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
    $("#password_reset_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
        rules: {
            email: {
                required: true,
                email: true,
            },
        },
        messages:{
            email:{
                remote: "This email address is not registered."
            }
        }
    });
});
