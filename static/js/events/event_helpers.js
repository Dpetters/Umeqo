function get_parent(element){
    var parent = null;
    console.log(typeof(EVENT_PAGE));
    if (typeof(EVENT_PAGE)!="undefined"){
        console.log("here");
        parent = $(".event");
    }else{
        parent = $(element).parents(".event_snippet");
    }
    console.log(parent);
    return parent;
}