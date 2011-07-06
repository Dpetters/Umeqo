$(document).ready(function(){
	
    $('#deactivate_account_link').click( function () {
        deactivate_account_dialog = open_deactivate_account_dialog();
        deactivate_account_dialog.html(dialog_ajax_loader);

        var deactivate_account_dialog_timeout = setTimeout(show_long_load_message_in_dialog, 10000);
        $.ajax({
            dataType: "html",
            url: EMPLOYER_DEACTIVATE_ACCOUNT_URL,
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(deactivate_account_dialog_timeout);
                switch(jqXHR.status){
                    case 0:
                        deactivate_account_dialog.html(dialog_check_connection_message);
                        break;
                    default:
                        deactivate_account_dialog.html(dialog_error_message);
                }
            },
            success: function (data) {
                clearTimeout(deactivate_account_dialog_timeout);

                deactivate_account_dialog.html(data);
                deactivate_account_dialog.dialog('option', 'position', 'center');
            }
        });
    });
});