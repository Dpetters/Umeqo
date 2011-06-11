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
                    $("#login_form .error_section").html("");
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
                               $("#login_form .error_section").html(data.error);
                            break;
                        case true:
                            window.location = data.success_url;
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
            },
            password: {
                required: true
            }
        },
    });
    
    if(get_parameter_by_name("next")){
        $(".login_link").click();    
    }
});