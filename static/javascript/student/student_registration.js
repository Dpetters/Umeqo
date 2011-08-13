$(document).ready( function() {
    var registration_xhr = null;
    $.validator.addMethod('isMITEmail', function(value, element) {
        // For testing, allow umeqo.com emails as well.
        return (value.length - "mit.edu".length) == value.indexOf("mit.edu") ||
                (value.length - "umeqo.com".length) == value.indexOf("umeqo.com");

    });
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
                	$("#student_registration_form input[type=submit]").removeAttr('disabled');
                    hide_form_submit_loader("#student_registration_form");
                },
                success: function(data) {
                    if(data.valid){
           				window.location = data.success_url + "?email=" + data.email;
                    }else{
                        if (data.form_errors.email){
                            var element = $("#id_email");
                            element.css('border', '1px solid red').focus().val("");
                            place_errors_ajax_table(data.form_errors.email, element);
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
                    url:"/check-email-availability/",
                    error: errors_in_message_area_handler
                },
            },
            password1: {
                required: true,
                minlength: PASSWORD_MIN_LENGTH,
            }
        },
        messages:{
            email:{
                required: "What's your email?",
                email: "Doesn't look like a valid email.",
                isMITEmail: 'Must be an MIT email.',
                remote: EMAIL_ALREADY_REGISTERED_MESSAGE
            },
            password1: {
                required: 'You need a password!'
            }
        }
    });
});
