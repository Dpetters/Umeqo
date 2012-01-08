function open_transaction_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        dialogClass: "transaction_dialog",
        modal:true,
        width:575,
        resizable: false,
        close: function() {
            transaction_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function handle_open_transaction_dialog_link_click(e){
    transaction_dialog = open_transaction_dialog();
    transaction_dialog.dialog("option", "title", $(this).attr("data-title"));
    transaction_dialog.html(DIALOG_AJAX_LOADER);

    var transaction_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    var json_data = {'action':$(this).attr("data-action"), 'subscription_type':$(this).attr("data-subscription-type")}
    
    $.ajax({
        type:'GET',
        dataType: "html",
        url: SUBSCRIPTION_TRANSACTION_URL,
        data: json_data,
        complete: function(jqXHR, textStatus) {
            clearTimeout(transaction_dialog_timeout);
            transaction_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                transaction_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                transaction_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            transaction_dialog.html(data);
            subscription_form_validator = $("#subscription_form").validate({
                submitHandler: function (form) {
                    $(form).ajaxSubmit({
                        url: SUBSCRIPTION_TRANSACTION_URL,
                        data: json_data,
                        dataType: 'json',
                        beforeSubmit: function (arr, $form, options) {
                            $("#subscription_form input[type=submit]").attr("disabled", "disabled");
                            show_form_submit_loader("#subscription_form");
                            $("#subscription_form .errorspace, #subscription_form .error_section").html("");
                        },
                        complete : function(jqXHR, textStatus) {
                            transaction_dialog.dialog('option', 'position', 'center');
                            $("#subscription_form input[type=submit]").removeAttr("disabled");
                            hide_form_submit_loader("#subscription_form");
                        },
                        error: function(jqXHR, textStatus, errorThrown){
                            if(jqXHR.status==0){
                                $(".transaction_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                            }else{
                                $(".transaction_dialog .error_section").html(ERROR_MESSAGE);
                            }
                        },
                        success: function (data) {
                            if(data.errors) {
                                place_table_form_errors("#subscription_form", data.errors);
                            } else {
                                var success_message = "<div class='message_section'><p>We have received your request and will get back to you ASAP. Thank you!.</p></div>";
                                success_message += CLOSE_DIALOG_LINK;
                                transaction_dialog.dialog("option", "title", "Request Submitted");
                                transaction_dialog.html(success_message);
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
                    },
                    employer: {
                        required: true
                    },
                    employer_size: {
                        required: true
                    },
                },
                messages: {
                    email: {
                        email: "Please enter a valid email."
                    }
                }
            });
        }
    });
}
$(document).ready( function() {
    $('.open_transaction_dialog_link.upgrade, .open_transaction_dialog_link.extend, .open_transaction_dialog_link.subscribe, .open_transaction_dialog_link.cancel').click(handle_open_transaction_dialog_link_click);
});