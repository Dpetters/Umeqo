/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {

	/* Login Dialog */
	var create_login_dialog = function () {
	    var $login_dialog = $('<div class="dialog"></div>')
		.dialog({
			autoOpen: false,
			title: "Login",
			dialogClass: "login_dialog",
			resizable: false,
			modal: true,
			width: 600,
			close: function() {
				$login_dialog.remove();
			}
		});
		$login_dialog.dialog('open');
		return $login_dialog;
	};
	
	$('.login_link').live('click', function () {
		var $login_dialog = create_login_dialog();
		$login_dialog.html(ajax_loader);

		var login_dialog_timeout = setTimeout(show_loading_failed_message, 10000);
		$.ajax({
			dataType: "html",
			url: '/login_dialog/?next=' + get_parameter_by_name('next'),
			success: function (data) {
				clearTimeout(login_dialog_timeout);

				$login_dialog.html(data);
				$("#id_username").focus();
				$login_dialog.dialog('option', 'position', 'center');

				format_required_labels("#login_form");
				align_form("#login_form");

				login_form_validator = $("#login_form").validate({
					submitHandler: function(form) {
						$(form).ajaxSubmit({
							dataType: 'json',
							beforeSubmit: function (arr, $form, options) {
								show_form_submit_loader("#login_form");
							},
							error: function(jqXHR, textStatus, errorThrown) {
								var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"' + textStatus + '"</strong></div>';
								error_message_details += close_dialog_link;
								$login_dialog.html(error_message_template + error_message_details);
							},
							success: function(data) {
								hide_form_submit_loader("#login_form");
								switch(data) {
									case "invalid":
										$("#dialog_form_error_section").html("<p class=error>The password you entered was not correct.<br\> Note that it is case-sensitive.</p>");
										$("#login_form_submit_button_wrapper").css("margin-top", 15);
										break;
									case "inactive":
										$("#dialog_form_error_section").html("<p class=error>This account has been suspended.<br/> Please direct all inquiries to admin@sbconnect.org.</p>");
										$("#login_form_submit_button_wrapper").css("margin-top", 15);
										break;
									case "cookies_disabled":
										$("#dialog_form_error_section").html("<p class=error>Your browser doesn't seem to have cookies enabled.<br/> Cookies are required to login.</p>");
										$("#login_form_submit_button_wrapper").css("margin-top", 15);
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
						username: {
							required: true,
							remote: "/check_username_existence/"
						},
						password: {
							required: true
						}
					},
					messages:{
						username:{
							remote: "This username is not registered"
						}
					}
				});
			},
		});
	});
	
	if(get_parameter_by_name("next")){
		$(".login_link").click();	
	}
});