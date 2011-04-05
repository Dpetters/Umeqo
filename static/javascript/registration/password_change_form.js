/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	// Password Change Form Validation
	$("#password_change_form").validate({
		highlight: highlight,
		unhighlight: unhighlight,
		errorPlacement: place_errors,
		rules: {
			old_password: {
				required: true,
				remote: "/check_password",
			},
			new_password1: {
				required: true,
			},
			new_password2:{
				required: true,
				equalTo: '#id_new_password1'
			},
		},
		messages:{
			old_password: {
				remote: "Incorrect password."
			},
			new_password2:{
				equalTo: "The passwords you entered don't match."
			}
		}
	});

	format_required_labels("#password_change_form");
	align_form("#password_change_form");
});
