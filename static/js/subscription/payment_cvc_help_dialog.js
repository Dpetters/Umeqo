var open_cvc_help_dialog = function () {
    var cvc_help_dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title: "What's a CSC?",
        dialogClass: "payment_cvc_help_dialog",
        resizable: false,
        modal: true,
        width: 575,
        close: function() {
            cvc_help_dialog.remove();
        }
    });
    cvc_help_dialog.dialog('open');
    return cvc_help_dialog;
};

$('.open_cvc_help_dialog_link').live('click', function (e) {

    cvc_help_dialog = open_cvc_help_dialog();
    cvc_help_dialog.html(DIALOG_AJAX_LOADER);

    var cvc_help_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        dataType: "html",
        url: PAYMENT_CVC_HELP_URL,
        complete : function(jqXHR, textStatus) {
            clearTimeout(cvc_help_dialog_timeout);
            cvc_help_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                cvc_help_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                cvc_help_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            cvc_help_dialog.html(data);
        }
    });
    e.preventDefault();
});