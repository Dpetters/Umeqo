/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	$("#id_username").focus( function() {
		$(".below_header_message").slideUp();
	});
	$("#id_password").focus( function() {
		$(".below_header_message").slideUp();
	});

});