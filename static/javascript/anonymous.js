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
    
    var login_form_validator = $("#login_form").validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                data: {next: get_parameter_by_name('next')},
                beforeSubmit: function (arr, $form, options) {
                    show_form_submit_loader("#login_form");
                },
                error: function(jqXHR, textStatus, errorThrown) {
                        hide_form_submit_loader("#login_form");
                    switch(jqXHR.status){
                        case 0:
                            $("#login_form .error_section").html(form_check_connection_message);
                            break;
                        default:
                            show_error_dialog(page_error_message);
                    }
                },
                success: function(data) {
                    hide_form_submit_loader("#login_form");
                    switch(data.valid) {
                        case false:
                               switch(data.reason) {
                                case "invalid":
                                    $("#login_form .error_section").html("<p class=error>This username and password combo is invalid. Note that both are case-sensitive.</p>");
                                    break;
                                case "inactive":
                                    $("#login_form .error_section").html("<p class=error>This account has been suspended. Please direct all inquiries to admin@umeqo.com.</p>");
                                    break;
                                case "cookies_disabled":
                                    $("#login_form .error_section").html("<p class=error>Your browser doesn't seem to have cookies enabled. Cookies are required to login.</p>");
                                    break;
                                default:
                                    show_error_dialog(page_error_message);
                                    break;
                            }
                            break;
                        case true:
                            window.location = data.url;
                            break;
                        default:
                            show_error_dialog(page_error_message);
                            break;
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
                /*
                remote: {
                    url:"/check-username-existence/",
                    error: function(jqXHR, textStatus, errorThrown) {
                        switch(jqXHR.status){
                            case 0:
                                $("#login_form .error_section").html(form_check_connection_message);
                                break;
                            default:
                                show_error_dialog(page_error_message);
                        }
                    },
                }
                */
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