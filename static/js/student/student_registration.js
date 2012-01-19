$(document).ready( function() {
    $("#student_registration_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                    $("#student_registration_form input[type=submit]").attr('disabled', 'disabled');
                    show_form_submit_loader("#student_registration_form");
                    $("#student_registration_form .error_section").html("");
                },
                complete : function(jqXHR, textStatus) {
                    $("#student_registration_form input[type=submit]").removeAttr('disabled').focusout();
                    hide_form_submit_loader("#student_registration_form");
                },
                success: function(data) {
                    if(data.errors){
                        place_table_form_errors("#student_registration_form", data.errors);
                        if (data.errors.email){
                            $("#id_email").val("").focus();
                        }
                    }else{
                        window.location = data.success_url + "?email=" + data.email;
                    }
                },
                error: errors_in_message_area_handler
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            email: {
                required: true,
                email: true,
                isMITEmail: true,
                remote: {
                    dataType: 'json',
                    url: CHECK_EMAIL_AVAILABILITY_URL,
                    error: errors_in_message_area_handler
                }
            },
            password: {
                required: true,
                minlength: PASSWORD_MIN_LENGTH
            }
        },
        messages:{
            email:{
                required: EMAIL_REQUIRED,
                email: INVALID_EMAIL,
                isMITEmail: MUST_BE_MIT_EMAIL,
                remote: EMAIL_ALREADY_REGISTERED
            },
            password: {
                required: PASSWORD_REQUIRED
            }
        }
    });

    function open_registration_help_dialog(){
        var dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Trouble Registering?",
            dialogClass: "registration_help_dialog",
            modal:true,
            resizable: false,
            width:484,
            close: function() {
                $(".registration_help_dialog").remove();
            }
        });
        dialog.dialog('open').html(DIALOG_AJAX_LOADER).dialog('option', 'position', 'center');
        return dialog;
    };
    
    $(".open_registration_help_dialog_link").click(function(){
        var $registration_help_dialog = open_registration_help_dialog();
        var registration_help_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: STUDENT_REGISTRATION_HELP_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(registration_help_dialog_timeout);
                $registration_help_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    $registration_help_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    $registration_help_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                $registration_help_dialog.html(data);
            }
        });    
    });

});