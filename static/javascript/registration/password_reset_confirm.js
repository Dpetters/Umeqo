/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	// Password Reset Confirm Form Validation
	password_reset_form_validator = $("#password_reset_confirm_form").validate({
		highlight: function(element, errorClass) {
			highlight(element, errorClass);
		},
		unhighlight: unhighlight,
		errorPlacement: place_errors,
		rules: {
			new_password1: {
				required: true,
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

	// Form Alignment
	format_required_labels("#password_reset_confirm_form");
	align_form("#password_reset_confirm_form");
});
