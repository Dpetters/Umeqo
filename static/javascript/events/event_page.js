$(document).ready(function(){
    $('#attending-button').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            if (typeof data['valid']!='undefined' && data['valid']==true) {
                that.parent().fadeOut(200,function() {
                    var newText = $('<span>Attending</span>');
                    var newLink = $('<a href="" id="not-attending-button">RSVP: Not attending</a>');
                    newLink.attr('href',EVENT_UNRSVP_URL);
                    that.replaceWith(newText);
                    newText.after(newLink);
                });
                that.parent().fadeIn();
            }
        },"json");
        e.preventDefault();
    });
    $('#not-attending-button').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            if (typeof data['valid']!='undefined' && data['valid']==true) {
                that.parent().fadeOut(200,function() {
                    var newText = $('<a href="" id="attending-button" class="button">RSVP: Attending</a>');
                    newText.attr('href',EVENT_RSVP_URL);
                    that.replaceWith(newText);
                    $('#event_rsvp span').remove();
                });
                that.parent().fadeIn();
            }
        },"json");
        e.preventDefault();
    });
});
