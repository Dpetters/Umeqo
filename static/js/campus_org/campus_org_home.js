$(document).ready( function () {
    $('.delete-event-link').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            var li = that.parentsUntil('ul')
            li.slideUp(function(){
                li.remove();
                if ($('.event_list:eq(0) li').length==0) {
                    $('#no_events_block').slideDown();
                }
            });
        });
        e.preventDefault();
    });
});
