$(document).ready( function () {
    $('.delete-event-link').live('click',function(e) {
        var $dialog = $('<div id="delete-event-dialog" class="dialog"><p>Are you sure you want to cancel this event?</p><p><a href="#" id="delete-event-confirm" class="button">Confirm</a></div>')
        .dialog({
            title:"Cancel Event",
            dialogClass: "event_cancel_dialog",
            modal:true,
            width:410,
            resizable: false,
            draggable: false
        });
        var that = this;
        $('#delete-event-confirm').click(function(e) {
            $dialog.remove();
            var li = $(that).parents("li");
            var ul = li.parent();
            $.post($(that).attr('href'),function(data) {
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
            });
            e.preventDefault();
        });
        e.preventDefault();
    });
});
