/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
*/

$(document).ready( function() {
    $.validator.addMethod('isMITEmail', function(value, element) {
        return (value.length - "mit.edu".length) == value.indexOf("mit.edu");
    });
    $("#student_registration_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                    show_form_submit_loader("#student_registration_form");
                    $("#student_registration_form .error_section").html("");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    hide_form_submit_loader("#student_registration_form");
                    switch(jqXHR.status){
                        case 0:
                            if (errorThrown.slice(0, 12-errorThrown.length)=="Invalid JSON"){
                                $("#student_registration_block .main_block_content").html(page_error_message);
                            }
                            $("#student_registration_form .error_section").html(form_check_connection_message);
                            break;
                        default:
                            $("#student_registration_block .main_block_content").html(page_error_message);
                    }
                },
                success: function(data) {
                    hide_form_submit_loader("#student_registration_form");
                    switch(data.valid) {
                        case false:
                            if (data.form_errors.email){
                                element = $("#id_email");
                                element.css('border', '1px solid red').focus().val("");
                                place_errors_ajax_table(data.form_errors.email, element);
                            }
                            else if (data.form_errors.__all__){
                                place_non_field_ajax_errors(data.form_errors.__all__, "#student_registration_form");
                                if(data.form_errors.__all__[0] == PASSWORDS_DONT_MATCH_MESSAGE){
                                    $("#id_password1").css('border', '1px solid red').focus().val("");
                                    $("#id_password2").css('border', '1px solid red').val("");                                    
                                }
                            }
                            break;
                        case true:
                            window.location.replace(data.success_url);
                            break;
                        defaultfalse:
                            $("#student_registration_block .main_block_content").html(page_error_message);
                            break;
                    }
                }
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
        rules: {
            email: {
                required: true,
                email: true,
                isMITEmail: true,
                remote: {
                    dataType: 'json',
                    url:"/check-email-availability/",
                    error: function(jqXHR, textStatus, errorThrown) {
                        switch(jqXHR.status){
                            case 0:
                                if (errorThrown.slice(0, 12-errorThrown.length)=="Invalid JSON"){
                                    $("#student_registration_block .main_block_content").html(page_error_message);
                                }
                                $("#student_registration_form .error_section").html(form_check_connection_message);
                                break;
                            default:
                                $("#student_registration_block .main_block_content").html(page_error_message);
                        }
                    },
                },
            },
            password1: {
                required: true,
            },
            password2:{
                required: true,
                equalTo: '#id_password1',
            },
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
            },
            password2: {
                required: 'A second time, just to check.',
                equalTo: "Passwords don't match."
            }
        }
    });
});
