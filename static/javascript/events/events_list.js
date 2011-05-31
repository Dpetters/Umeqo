$(document).ready(function(){
    var timeoutID;
    function filterEvents() {
        var query = $('#event_search_query').val();
        $('.main_block_content').append('<div id="loading_div"></div>');
        $.get(SEARCH_URL,{'q':query},function(data) {
            $('#main_event_list').html(data);
            $('#loading_div').remove();
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
        if (event.state != null && event.state.q!="") $('#event_search_query').val(event.state.q);
        else $('#event_search_query').val("");
        filterEvents();
    }
});
