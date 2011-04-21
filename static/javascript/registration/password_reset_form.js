/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
	// Password Reset Form Validation
	$("#password_reset_form").validate({
		highlight: highlight,
		unhighlight: unhighlight,
		errorPlacement: place_errors,
		rules: {
			email: {
				required: true,
				email: true,
				remote: {
					url: "/check-email-existence/",
					beforeSend: function() {
						$("#password_reset_form label.error").css("display", "none");
					}
				}
			},
		},
		messages:{
			email:{
				remote: "This email address is not registered."
			}
		}
	});

	format_required_labels("#password_reset_form");
	align_form("#password_reset_form");
});