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
        var query = $('#event_search_query').val();
        history.pushState({'q':query},"search","?q="+query);
    });
    $('#event_search_query').keydown(function() {
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(filterEvents,500);
    });
    
    window.onpopstate = function(event) {
        $('#event_search_query').val(event.state.q);
    }
});