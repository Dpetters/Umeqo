function request_account() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title: "Umeqo Account Request",
        dialogClass: "account_request_dialog",
        modal:true,
        width:575,
        resizable: false,
        close: function() {
            account_request_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function handle_request_account_link_click(e){
    account_request_dialog = request_account();
    account_request_dialog.dialog("option", "title", $(this).attr("data-dialog-title"));
    account_request_dialog.html(DIALOG_AJAX_LOADER);

    var account_request_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    var data = {'subscription_type':$(this).data("subscription-type")}
    $.ajax({
        type:'GET',
        dataType: "html",
        url: ACCOUNT_REQUEST_URL,
        data: data,
        complete: function(jqXHR, textStatus) {
            clearTimeout(account_request_dialog_timeout);
            account_request_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                account_request_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                account_request_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            account_request_dialog.html(data);

            account_request_form_validator = $("#account_request_form").validate({
                submitHandler: function (form) {
                    $(form).ajaxSubmit({
                        url: ACCOUNT_REQUEST_URL,
                        data: data,
                        dataType: 'json',
                        beforeSubmit: function (arr, $form, options) {
                            $("#account_request_form input[type=submit]").attr("disabled", "disabled");
                            show_form_submit_loader("#account_request_form");
                            $("#account_request_form .errorspace, #account_request_form .error_section").html("");
                        },
                        complete : function(jqXHR, textStatus) {
                            account_request_dialog.dialog('option', 'position', 'center');
                            $("#account_request_form input[type=submit]").removeAttr("disabled");
                            hide_form_submit_loader("#account_request_form");
                        },
                        error: function(jqXHR, textStatus, errorThrown){
                            if(jqXHR.status==0){
                                $(".account_request_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                            }else{
                                $(".account_request_dialog .error_section").html(ERROR_MESSAGE);
                            }
                        },
                        success: function (data) {
                            if(data.errors) {
                                place_table_form_errors("#account_request_form", data.errors);
                            } else {
                                var success_message = "<div class='message_section'><p>We have received your request and will get back to you ASAP. Thank you!.</p></div>";
                                success_message += CLOSE_DIALOG_LINK;
                                account_request_dialog.dialog("option", "title", "Account Request Submitted");
                                account_request_dialog.html(success_message);
                            }
                        }
                    });
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    recruiter_name: {
                        required: true
                    },
                    recruiter_email: {
                        required: true,
                        email: true
                    },
                    employer_name: {
                        required: true
                    },
                    message_body: {
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
    $('.request_account_link').click(handle_request_account_link_click);
});