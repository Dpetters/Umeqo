var message = "";

var open_contact_us_dialog = function () {
    var contact_us_dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title: "Contact Us",
        dialogClass: "contact_us_dialog",
        resizable: false,
        modal: true,
        width: 610,
        close: function() {
            contact_us_dialog.remove();
        }
    });
    contact_us_dialog.dialog('open');
    return contact_us_dialog;
};

$('.open_contact_us_dialog_link').live('click', function (e) {
    message = $(this).data("message");
    
    for(var i = 0; i < $(".dialog").length; i++){
           $($(".dialog")[i]).remove();        
    
    }
    contact_us_dialog = open_contact_us_dialog();
    contact_us_dialog.html(DIALOG_AJAX_LOADER);

    var contact_us_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        dataType: "html",
        data: {'message': message},
        url: CONTACT_US_URL,
        complete : function(jqXHR, textStatus) {
            clearTimeout(contact_us_dialog_timeout);
            contact_us_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                contact_us_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                contact_us_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            contact_us_dialog.html(data);
            contact_us_form_validator = $("#contact_us_form").validate({
                submitHandler: function (form) {
                    $(form).ajaxSubmit({
                        url: CONTACT_US_URL,
                        dataType: 'json',
                        beforeSubmit: function (arr, $form, options) {
                            $("#contact_us_form input[type=submit]").attr("disabled", "disabled");
                            show_form_submit_loader("#contact_us_form");
                            $("#contact_us_form .errorspace, #contact_us_form .error_section").html("");
                        },
                        complete : function(jqXHR, textStatus) {
                            contact_us_dialog.dialog('option', 'position', 'center');
                            $("#contact_us_form input[type=submit]").removeAttr("disabled");
                            hide_form_submit_loader("#contact_us_form");
                        },
                        error: function(jqXHR, textStatus, errorThrown){
                            errors_in_dialog_error_section("contact_us_dialog", jqXHR, textStatus, errorThrown);
                        },
                        success: function (data) {
                            if(data.valid) {
                                var success_message = "<div class='message_section'><p>" + THANK_YOU_FOR_CONTACTING_US_MESSAGE + "</p></div>";
                                success_message += CLOSE_DIALOG_LINK;
                                contact_us_dialog.html(success_message);
                            } else {
                                place_table_form_errors("#contact_us_form", data.errors);
                            }
                        }
                    });
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    name: {
                        required: true
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    body: {
                        required: true
                    }
                },
                messages: {
                    email: {
                        email: "Please enter a valid email."
                    }
                }
            });
        }
    });
    e.preventDefault();
});