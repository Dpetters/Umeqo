$(document).ready( function() {
    // If logged in, hide login form and turn on timeout.
    // If not logged in, show login form
    $("#id_username").focus( function() {
        $(".below_header_message").slideUp();
    });
    $("#id_password").focus( function() {
        $(".below_header_message").slideUp();
    });
});