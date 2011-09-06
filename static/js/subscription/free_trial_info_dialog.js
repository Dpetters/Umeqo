$(document).ready( function() {
    function open_free_trial_info_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Umeqo Free Trial",
            dialogClass: "free_trial_info_dialog",
            modal:true,
            width:496,
            resizable: false,
            close: function() {
                free_trial_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('.open_ftid_link').click( function () {
        free_trial_info_dialog = open_free_trial_info_dialog();
        free_trial_info_dialog.html(DIALOG_AJAX_LOADER);

        var free_trial_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: FREE_TRIAL_INFO_DIALOG_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(free_trial_info_dialog_timeout);
                free_trial_info_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    free_trial_info_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    free_trial_info_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                free_trial_info_dialog.html(data);
            }
        });
    });
});