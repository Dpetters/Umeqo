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
                },
                error: function(jqXHR, textStatus, errorThrown){
                    hide_form_submit_loader("#student_registration_form");
            		switch(jqXHR.status){
            			case 500:
            				$("#student_registration_block .main_block_content").html(status_500_message);
            				break;
            			default:
            				$("#student_registration_form_error_section").html(check_connection_message);	
            		}
				},
                success: function(data) {
                    hide_form_submit_loader("#student_registration_form");
                    switch(data) {
                        case "notmit":
                            $("#student_registration_form_error_section").html("<p class='error'>Please use an mit.edu address.</p>");
                            $("#id_email").css('border', '1px solid red').focus().val("");
                            break;
                        case "notstudent":
                            $("#student_registration_form_error_section").html("<p class='error'>Please enter a valid MIT student's email address.</p>");
                            $("#id_email").css('border', '1px solid red').focus().val("");
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
                remote: {
                	url:"/check_email_availability/",
                	error: function(jqXHR, textStatus, errorThrown) {
	            		switch(jqXHR.status){
	            			case 500:
	            				$("#student_registration_block .main_block_content").html(status_500_message);
	            				break;
	            			default:
	            				$("#student_registration_form_error_section").html(check_connection_message);	
	            		}
                    },
                }
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