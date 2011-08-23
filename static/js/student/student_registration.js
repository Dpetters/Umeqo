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
                    if(data.valid){
                           window.location = data.success_url + "?email=" + data.email;
                    }else{
                        place_table_form_errors("#student_registration_form", data.errors);
                        if (data.errors.email){
                            $("#id_email").val("").focus();
                        }
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
                },
            },
            password1: {
                required: true,
                minlength: PASSWORD_MIN_LENGTH
            },
            invite_code: {
                required: true
       
            }
        },
        messages:{
            email:{
                required: EMAIL_REQUIRED,
                email: INVALID_EMAIL,
                isMITEmail: MUST_BE_MIT_EMAIL,
                remote: EMAIL_ALREADY_REGISTERED
            },
            password1: {
                required: PASSWORD_REQUIRED
            },
            invite_code: {
                required: INVITE_CODE_REQUIRED
            }
        }
    });
    
    $.validator.addMethod('isMITEmail', function(value, element) {
        // If testing, allow umeqo.com emails as well.
        if (DEBUG)
               return (value.length - "mit.edu".length) == value.indexOf("mit.edu") || (value.length - "umeqo.com".length) == value.indexOf("umeqo.com");
        else
            return (value.length - "mit.edu".length) == value.indexOf("mit.edu");
    });
});