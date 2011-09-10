$(document).ready( function () {
    $('.delete-event-link').live('click',function(e) {
        var li = $(this).parents("li");
        var ul = li.parent();
        $.post($(this).attr('href'),function(data) {
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
});
