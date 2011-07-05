$(document).ready( function () {
    $("#account_settings_tabs").tabs();

    $("#password_change_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                    show_form_submit_loader("#password_change_form");
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    hide_form_submit_loader("#password_change_form");
                    switch(jqXHR.status){
                        case 0:
                            $("#password_change_form .error_section").html(form_check_connection_message);
                            break;
                        default:
                            show_error_dialog(page_error_message);
                    }
                },
                success: function(data) {
                    hide_form_submit_loader("#login_form");
                    switch(data.valid) {
                        case false:
                        	place_form_errors("#login_form", data.errors);
                            if (data.errors.id_old_password){
                                $("#id_old_password").val("").css('border', '1px solid red').focus();
                            }
                            break;
                        case true:
                        	window.location.href = window.location.href + "?msg=password-changed"
                            break;
                        default:
                            show_error_dialog(page_error_message);
                            break;
                    }
                }
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
        rules: {
            old_password: {
                required: true,
            },
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