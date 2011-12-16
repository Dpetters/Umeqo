$(document).ready( function() {
    function open_free_subscription_info_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Umeqo Event Subscription",
            dialogClass: "free_subscription_info_dialog",
            modal:true,
            width:496,
            resizable: false,
            close: function() {
                free_subscription_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('.open_free_subscription_info_dialog_link').click( function () {
        free_subscription_info_dialog = open_free_subscription_info_dialog();
        free_subscription_info_dialog.html(DIALOG_AJAX_LOADER);

        var free_subscription_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: FREE_SUBSCRIPTION_INFO_DIALOG_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(free_subscription_info_dialog_timeout);
                free_subscription_info_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    free_subscription_info_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    free_subscription_info_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                free_subscription_info_dialog.html(data);
            }
        });
    });
});