/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
*/

$(document).ready( function() {

    format_required_labels("#student_registration_form");
    align_form("#student_registration_form");

    $("#student_registration_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                beforeSubmit: function (arr, $form, options) {
                    show_form_submit_loader("#student_registration_form");
                    $("#student_registration_form_error_section").html("");
                    $(".button_wrapper_with_margins").css("margin-top", "20px");
                },
                error: function(jqXHR, textStatus, errorThrown){
					var error_message_details = '<div class="message_section"><strong>Error Details</strong><br/><br/>"' + textStatus + '"</strong></div>';
					error_message_details += refresh_page_link;
					$("#student_registration_block .main_block_content").html(error_message_template + error_message_details);
				},
                success: function(data) {
                    hide_form_submit_loader("#student_registration_form");
                    switch(data) {
                        case "notmit":
                            $("#student_registration_form_error_section").html("<p class=error>Please use an mit.edu address.</p>");
                            $("#id_email").css('border', '1px solid red').focus().val("");
                            $(".button_wrapper_with_margins").css("margin-top", "15px");
                            break;
                        case "notstudent":
                            $("#student_registration_form_error_section").html("<p class=error>Please enter a valid MIT student's email address.</p>");
                            $("#id_email").css('border', '1px solid red').focus().val("");
                            $(".button_wrapper_with_margins").css("margin-top", "15px");
                            break;
                        default:
                            window.location.replace(data);
                    }
                }
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors,
        rules: {
            email: {
                required: true,
                email:true,
                remote: "/check_email_availability/",
            },
            password1: {
                required: true,
            },
            password2:{
                required: true,
                equalTo: '#id_password1'
            },
        },
        messages:{
            email:{
                remote: "This email is already registered."
            },
            password2:{
                equalTo: "The passwords you entered don't match."
            }
        }
    });
});