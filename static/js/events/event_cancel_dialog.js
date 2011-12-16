$(document).ready( function () {
    function open_event_cancel_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Confirm Cancellation",
            dialogClass: "event_cancel_dialog",
            modal:true,
            width:410,
            resizable: false,
            close: function() {
                event_cancel_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('.cancel_event_link').click( function (e) {
        var that = this;
        event_cancel_dialog = open_event_cancel_dialog();
        event_cancel_dialog.html(DIALOG_AJAX_LOADER);

        var event_cancel_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            data:{'event_id':$(that).data("event-id")},
            url: $(that).attr("href"),
            complete: function(jqXHR, textStatus) {
                clearTimeout(event_cancel_dialog_timeout);
                event_cancel_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    event_cancel_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    event_cancel_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                event_cancel_dialog.html(data);
                $('#event_cancel_confirm_link').click(function(e) {
                    var li = $(that).parents("li");
                    var ul = li.parent();
                    $.ajax({
                        type:"POST",
                        dataType: "json",
                        data:{'event_id':$(that).data("event-id")},
                        url: $(that).attr("href"),
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#event_cancel_form");
                        },
                        complete : function(jqXHR, textStatus) {
                            hide_form_submit_loader("#event_cancel_form");
                            event_cancel_dialog.dialog('option', 'position', 'center');
                        },
                        success: function (data){
                            event_cancel_dialog.remove();
                            if (li.length != 0){
                                li.slideUp(function(){
                                    li.remove();
                                    if (ul.children().length == 0)
                                    {
                                        $("#past_events_header").addClass("no_top_margin");
                                        ul.prev().remove();
                                        ul.remove();
                                    }
                                    if ($('.event_list li').length==0) {
                                        $('#no_events_block').slideDown();
                                    }
                                });
                            }else{
                                window.location.href="/?msg=" + data.type + "-cancelled";
                            }
                            
                        }
                    });
                    e.preventDefault();
                });
            }
        });
        e.preventDefault();
    });
});