$(document).ready( function () {
    function open_rolling_deadline_end_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Confirm Rolling Deadline Ending",
            dialogClass: "rolling_deadline_end_dialog",
            modal:true,
            width:410,
            resizable: false,
            close: function() {
                rolling_deadline_end_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('.end_rolling_deadline_link').click( function (e) {
        var that = this;
        rolling_deadline_end_dialog = open_rolling_deadline_end_dialog();
        rolling_deadline_end_dialog.html(DIALOG_AJAX_LOADER);

        var rolling_deadline_end_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            data:{'event_id':$(that).data("event-id")},
            url: $(that).attr("href"),
            complete: function(jqXHR, textStatus) {
                clearTimeout(rolling_deadline_end_dialog_timeout);
                rolling_deadline_end_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    rolling_deadline_end_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    rolling_deadline_end_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                rolling_deadline_end_dialog.html(data);
                $('#rolling_deadline_end_confirm_link').click(function(e) {
                    var li = $(that).parents("li");
                    var ul = li.parent();
                    $.ajax({
                        type:"POST",
                        dataType: "json",
                        url: $(that).attr("href"),
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#rolling_deadline_end_form");
                        },
                        complete : function(jqXHR, textStatus) {
                            hide_form_submit_loader("#rolling_deadline_end_form");
                            rolling_deadline_end_dialog.dialog('option', 'position', 'center');
                        },
                        success: function (data){
                            rolling_deadline_end_dialog.remove();
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
                                $("#message_area").html("<p>" + ROLLING_DEADLINE_ENDED + "</p>");
                            }else{
                                window.location.href="/?msg=rolling-deadline-ended";
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