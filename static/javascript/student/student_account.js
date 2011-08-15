$(document).ready( function() {

    function open_account_deactivate_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Deactivate Account",
            dialogClass: "account_deactivate_dialog",
            modal:true,
            width:418,
            resizable: false,
            close: function() {
                account_deactivate_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#account_deactivate_link').click( function () {
        account_deactivate_dialog = open_account_deactivate_dialog();
        account_deactivate_dialog.html(DIALOG_AJAX_LOADER);

        var account_deactivate_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: STUDENT_ACCOUNT_DEACTIVATE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(account_deactivate_dialog_timeout);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    account_deactivate_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    account_deactivate_dialog.html(ERROR_MESSAGE_DIALOG);
                }
                account_deactivate_dialog.dialog('option', 'position', 'center');
            },
            success: function (data) {
                account_deactivate_dialog.html(data);
                account_deactivate_dialog.dialog('option', 'position', 'center');
                $("#student_deactivate_account_link").click(function(){
                	$.ajax({
                		type:"POST",
			            dataType: "json",
			            data:{'suggestion':$("#id_suggestion").val()},
			            url: STUDENT_ACCOUNT_DEACTIVATE_URL,
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#student_account_deactivate_form");
                        },
                        complete : function(jqXHR, textStatus) {
                        	hide_form_submit_loader("#student_account_deactivate_form");
                        },
			            error: function(jqXHR, textStatus, errorThrown) {
			                if(jqXHR.status==0){
			                    account_deactivate_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
			                }else{
			                    account_deactivate_dialog.html(ERROR_MESSAGE_DIALOG);
			                }
			                account_deactivate_dialog.dialog('option', 'position', 'center');
			            },
			            success: function (data) {
			                window.location.href = "/?action=account-deactivated";
			            }
			        });
			    });
            }
        });
    });
});