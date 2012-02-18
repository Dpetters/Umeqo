function get_parent(element){
    var parent = null;
    if (typeof(EVENT_PAGE)!="undefined"){
        parent = $("#event");
    }else{
        parent = $(element).parents(".event_snippet");
    }
    return parent;
}