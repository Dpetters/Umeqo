$(document).ready(function(){
	
    $('#account_deactivate_link').click( function () {
        account_deactivate_dialog = open_account_deactivate_dialog();
        account_deactivate_dialog.html(DIALOG_AJAX_LOADER);

        var account_deactivate_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: EMPLOYER_account_deactivate_URL,
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(account_deactivate_dialog_timeout);
                switch(jqXHR.status){
                    case 0:
                        account_deactivate_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                        break;
                    default:
                        account_deactivate_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                clearTimeout(account_deactivate_dialog_timeout);

                account_deactivate_dialog.html(data);
                account_deactivate_dialog.dialog('option', 'position', 'center');
            }
        });
    });
});