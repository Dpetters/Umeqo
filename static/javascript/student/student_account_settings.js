$(document).ready( function() {

    function open_deactivate_account_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Deactivate Account",
            dialogClass: "deactivate_account_dialog",
            modal:true,
            width:475,
            resizable: false,
            close: function() {
                deactivate_account_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#deactivate_account_link').click( function () {
        deactivate_account_dialog = open_deactivate_account_dialog();
        deactivate_account_dialog.html(DIALOG_AJAX_LOADER);

        var deactivate_account_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: STUDENT_DEACTIVATE_ACCOUNT_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(deactivate_account_dialog_timeout);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    deactivate_account_dialog.html(dialog_check_connection_message);
                }else{
                    deactivate_account_dialog.html(dialog_error_message);
                }
                deactivate_account_dialog.dialog('option', 'position', 'center');
            },
            success: function (data) {
                deactivate_account_dialog.html(data);
                deactivate_account_dialog.dialog('option', 'position', 'center');
            }
        });
    });
});