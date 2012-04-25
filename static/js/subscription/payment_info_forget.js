function open_payment_info_forget_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"Forget Payment Info",
        dialogClass: "payment_info_forget_dialog",
        modal:true,
        width:475,
        resizable: false,
        close: function() {
            payment_info_forget_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
}

function payment_info_forget_link_click_handler() {
    payment_info_forget_dialog = open_payment_info_forget_dialog();
    payment_info_forget_dialog.html(DIALOG_AJAX_LOADER);

    var payment_info_forget_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        dataType: "html",
        url: PAYMENT_INFO_FORGET_URL,
        complete: function(jqXHR, textStatus) {
            clearTimeout(payment_info_forget_dialog_timeout);
            payment_info_forget_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                payment_info_forget_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                payment_info_forget_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            payment_info_forget_dialog.html(data);
            $("#payment_info_forget_confirmation_link").click(function(){
                $.ajax({
                    type:"POST",
                    dataType: "json",
                    beforeSend: function (arr, $form, options) {
                        show_form_submit_loader(".payment_info_forget_dialog");
                    },
                    complete : function(jqXHR, textStatus) {
                        hide_form_submit_loader(".payment_info_forget_dialog");
                        payment_info_forget_dialog.dialog('option', 'position', 'center');
                    },
                    url: PAYMENT_INFO_FORGET_URL,
                    success: function (data){
                        window.location.href = "/";
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        if(jqXHR.status==0){
                            payment_info_forget_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                        }else{
                            payment_info_forget_dialog.html(ERROR_MESSAGE_DIALOG);
                        }
                    }
                });
            });
        }
    });
}


$(document).ready(function(){
    $(".payment_info_forget_link").click( payment_info_forget_link_click_handler);    
})
