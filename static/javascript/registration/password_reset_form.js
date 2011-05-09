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
				remote: {
                    url:"/check-email-existence/",
                 	beforeSend: function() {
						$("#password_reset_form label.error").css("display", "none");
					},
                    error: function(jqXHR, textStatus, errorThrown) {
                        switch(jqXHR.status){
                            case 0:
                            	$("#password_reset_form .error_section").html(form_check_connection_message);
                                break;
                            default:
                            	$("#password_reset_block .main_block_content").html(page_error_message);
                        }
                    },
                }
			},
		},
		messages:{
			email:{
				remote: "This email address is not registered."
			}
		}
	});
});