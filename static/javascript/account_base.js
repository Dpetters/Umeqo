$(document).ready( function () {
    $("#preferences_form_tabs").tabs();
    
    $("#global_email_checkbox").click(function(){
        if (this.checked)
            $("#notification_preferences_table input[type=checkbox]").attr('checked', true);
        else
            $("#notification_preferences_table input[type=checkbox]").attr('checked', false);
    });
    
    $("#preferences_form").submit(function(){
        $(this).ajaxSubmit({
            dataType: 'json',
            beforeSubmit: function (arr, $form, options) {
                $("#message_area").html("");
                show_form_submit_loader("#preferences_form");
            },
            complete: function(jqXHR, textStatus) {
                hide_form_submit_loader("#preferences_form");
            },
            error: function(jqXHR, textStatus, errorThrown){
                if(jqXHR.status==0){
                    $("#preferences_form .error_section").html(form_check_connection_message);
                }else{
                    show_error_dialog(page_error_message);
                }
            },
            success: function(data) {
                $("#message_area").html("<p>Preferences Saved.</p>");
            }
        });
        return false;
    });
    
    $("#password_change_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                    $("#message_area").html("");
                    show_form_submit_loader("#password_change_form");
                },
                complete: function(jqXHR, textStatus) {
                    hide_form_submit_loader("#password_change_form");
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if(jqXHR.status==0){
                        $("#password_change_form .error_section").html(form_check_connection_message);
                    }else{
                        show_error_dialog(page_error_message);
                    }
                },
                success: function(data) {
                    if(data.valid) {
                        if (get_parameter_by_name('msg') == "password-changed"){
                            window.location.reload();
                        }else{
                            window.location.href = window.location.href + "?msg=password-changed"
                        }
                    }else{
                        place_table_form_errors("#login_form", data.errors);
                        if (data.errors.id_old_password){
                            $("#id_old_password").val("").css('border', '1px solid red').focus();
                        }
                    }
                }
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
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
                equalTo: PASSWORDS_DONT_MATCH
            }
        }
    });
});