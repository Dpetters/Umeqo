/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {
    
    //toggle show/hide login form
    $('#login_button').click(function(){
        $('#loginWrapper').fadeToggle('fast',function(){
            $('#id_username').focus();
        });
    });
    $('#loginWrapper').hide();
    $(document).click(function(e) {
        if ($(e.target).parents('#loginWrapper').length == 0 &&
            $(e.target).parent().attr('id') != 'login_button') {
            $('#loginWrapper').hide();
        }
    });
    
    var login_form_validator = $('#login_form').validate({
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                data: {next: get_parameter_by_name('next')},
                beforeSubmit: function (arr, $form, options) {
                    $('#login_form .error_section').html('');
                    show_form_submit_loader('#login_form');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    hide_form_submit_loader("#login_form");
                    if (jqXHR.status == 0) {
                        $('#login_form .error_section').html(form_check_connection_message);
                    } else {
                        show_error_dialog(page_error_message);
                    }
                },
                success: function(data) {
                    hide_form_submit_loader('#login_form');
                    if (data.valid) {
                        document.location = data.success_url;
                    } else {
                        $("#login_form .error_section").html(data.error);
                    }
                }
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_login,
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true
            }
        },
        messages: {
            username: 'Enter your email.',
            password: 'You need a password!',
        }
    });
    
    if(get_parameter_by_name("next")){
        $(".login_link").click();    
    }
});
