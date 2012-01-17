function filter_events(data, disable_push){
    var data = data || "";
    var disable_push = disable_push || false;
    
    if(disable_push){
        $('#event_filtering_form #id_query').val(data.query);
        $("#event_filtering_form input[value=" + data.type + "]").attr("checked", "checked");
    }
    if(!data){
        data = {};
        data['query'] = $('#event_filtering_form #id_query').val();
        data['type'] = $("#event_filtering_form input[name=type]:checked").val()
    }
    $.ajax({
        url:window.location.pathname,
        data:data,
        beforeSend: function(){
               show_form_submit_loader("#event_filtering_form");
        },
        complete: function(jqXHR, textStatus){
            hide_form_submit_loader("#event_filtering_form");
        },
        success: function(html) {
            $('#event_list').html(html)
            if(!disable_push){
                history.pushState(data, "", window.location.pathname + "?query=" + data.query + "&type=" + data.type);
            }
        },
        error: errors_in_message_area_handler
    });    
}

window.onpopstate = function(event) {
    if (event.state != null) {
        filter_events(event.state, true);
    }else if ($('#isnotajax').val()=='false') {
        filter_events(INITIAL_STATE, true);
    }
}

$(document).ready(function(){
    var timeoutID;

    $('#event_filtering_form input[type=radio]').live('change',function() {
        filter_events();
    });
    
    $('#event_filtering_form #id_query').keydown(function() {
        var that = this;
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(function(){
            query = $(that).val();
            filter_events();
        },500);
    });
});
