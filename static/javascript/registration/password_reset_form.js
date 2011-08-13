$(document).ready( function() {
    $("#password_reset_form").validate({
    	/*
        submitHandler: function(form) {
            $(form).ajaxSubmit({
                dataType: 'json',
                beforeSubmit: function (arr, $form, options) {
                	$("#password_reset_form input[type=submit]").attr('disabled', 'disabled');
                    show_form_submit_loader("#password_reset_form");
                    $("#password_reset_form .error_section").html("");
                },
                complete : function(jqXHR, textStatus) {
                	$("#password_reset_form input[type=submit]").removeAttr('disabled');
                    hide_form_submit_loader("#password_reset_form");
                },
                success: function(data) {
                    if(data.valid){
           				window.location = data.success_url + "?email=" + data.email;
                    }else{
                        if (data.form_errors.email){
                            var element = $("#id_email");
                            element.css('border', '1px solid red').focus().val("");
                            place_errors_ajax_table(data.form_errors.email, element);
                        }
                    }
                },
                error: errors_in_message_area_handler
            });
        },*/
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            email: {
                required: true,
                email: true,
            },
        },
    });
});
