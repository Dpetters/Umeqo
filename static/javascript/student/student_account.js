$(document).ready( function() {

    function open_account_deactivation_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Account Deactivation",
            dialogClass: "account_deactivation_dialog",
            modal:true,
            width:420,
            resizable: false,
            close: function() {
                account_deactivation_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#account_deactivate_link').click( function () {
        account_deactivation_dialog = open_account_deactivation_dialog();
        account_deactivation_dialog.html(DIALOG_AJAX_LOADER);

        var account_deactivation_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: STUDENT_ACCOUNT_DEACTIVATE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(account_deactivation_dialog_timeout);
                account_deactivation_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    account_deactivation_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    account_deactivation_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                account_deactivation_dialog.html(data);
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
                    		account_deactivation_dialog.dialog('option', 'position', 'center');
                        },
			            error: function(jqXHR, textStatus, errorThrown) {
			                console.log(errorThrown);
			                if(jqXHR.status==0){
			                    account_deactivation_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
			                }else{
			                    account_deactivation_dialog.html(ERROR_MESSAGE_DIALOG);
			                }
			            },
			            success: function (data) {
			                console.log(data);
			                window.location.href = "/?action=account-deactivated";
			            }
			        });
			    });
            }
        });
    });
});