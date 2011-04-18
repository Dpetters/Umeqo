/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {
    
    //toggle show/hide login form
    $('#login_button').click(function(){
        $('#loginWrapper').fadeToggle("fast",function(){
            $("#id_username").focus();
        });
    });
    $('#loginWrapper').hide();
    
    // Login Form Validation
    $("#login_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                     show_form_submit_loader("#login_form");
                },
                success: function(data) {
                    hide_form_submit_loader("#login_form");
                    switch(data) {
                        case "invalid":
                            $("#login_form_error_section").html("<p class=error>Please enter a correct username and password. Note that both are case-sensitive.</p>");
                            $("#reset_password_link").css("margin-top", 5);
                            break;
                        case "inactive":
                            $("#login_form_error_section").html("<p class=error>This account has been suspended. Please direct all inquiries to admin@sbconnect.org.</p>");
                            $("#reset_password_link").css("margin-top", 5);
                            break;
                        case "cookies_disabled":
                            $("#login_form_error_section").html("<p class=error>Your browser doesn't appear to have cookies enabled. Cookies are required to login.</p>");
                            $("#reset_password_link").css("margin-top", 5);
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
                required: true
            },
            password: {
                required: true
            }
        }
    });
    
    var login_form_validator = $("#login_form").validate({
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
    
    if(get_parameter_by_name("next")){
        $(".login_link").click();    
    }
});