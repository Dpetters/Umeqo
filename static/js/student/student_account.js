$(document).ready( function() {

    function open_add() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Account Deactivation",
            dialogClass: "add",
            modal:true,
            width:440,
            resizable: false,
            close: function() {
                add.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#account_deactivate_link').click( function () {
        add = open_add();
        add.html(DIALOG_AJAX_LOADER);

        var add_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: STUDENT_ACCOUNT_DEACTIVATE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(add_timeout);
                add.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    add.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    add.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                add.html(data);
                $("#student_deactivate_account_link").click(function(){
                    $.ajax({
                        type:"POST",
                        dataType: "json",
                        data:{'suggestion':$("#id_suggestion").val()},
                        url: STUDENT_ACCOUNT_DEACTIVATE_URL,
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#student_account_deactivation_form");
                        },
                        complete : function(jqXHR, textStatus) {
                            hide_form_submit_loader("#student_account_deactivation_form");
                            add.dialog('option', 'position', 'center');
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            if(jqXHR.status==0){
                                add.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                            }else{
                                add.html(ERROR_MESSAGE_DIALOG);
                            }
                        },
                        success: function (data){
                            console.log(data);
                            if(data.errors){
                                place_table_form_errors("#student_account_deactivation_form", data.errors);  
                            }else{
                                window.location.href = "/?action=account-deactivated";
                            }
                        }
                    });
                });
            }
        });
    });
});