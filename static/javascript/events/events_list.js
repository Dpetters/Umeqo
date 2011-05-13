$(document).ready(function(){
    var timeoutID;
    function filterEvents() {
        var query = $('#event_search_query').val();
        $.get(SEARCH_URL,{'q':query},function(data) {
            $('#main_event_list').html(data);
            console.log('received');
        });
    }
    $('.name a').live('click',function() {
        history.pushState({},"search","?q="+$('#event_search_query').val());
    });
    $('#event_search_query').keydown(function() {
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(filterEvents,500);
    });
});