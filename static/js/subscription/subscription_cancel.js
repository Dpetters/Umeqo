$(document).ready(function(){
    function open_cancel_subscription_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Cancel Subscription",
            dialogClass: "csd",
            modal:true,
            width:440,
            resizable: false,
            close: function() {
                csd.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#cancel_subscription_link').click( function () {
        csd = open_cancel_subscription_dialog();
        csd.html(DIALOG_AJAX_LOADER);

        var csd_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CANCEL_SUBSCRIPTION_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(csd_timeout);
                csd.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    csd.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    csd.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                csd.html(data);
                $("#cancel_subscription_confirm_link").click(function(){
                    $.ajax({
                        type:"POST",
                        dataType: "json",
                        data: {'recruiter': $("#id_recruiter").val()},
                        url: CANCEL_SUBSCRIPTION_URL,
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#student_account_deactivation_form");
                        },
                        complete : function(jqXHR, textStatus) {
                            hide_form_submit_loader("#student_account_deactivation_form");
                            csd.dialog('option', 'position', 'center');
                        },
                        success: function (data){
                            if(data.errors){
                                place_table_form_errors("#student_account_deactivation_form", data.errors);  
                            }else{
                                window.location.href = "/?action=account-deactivated";
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            if(jqXHR.status==0){
                                csd.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                            }else{
                                csd.html(ERROR_MESSAGE_DIALOG);
                            }
                        }
                    });
                });
            }
        });
    });
});