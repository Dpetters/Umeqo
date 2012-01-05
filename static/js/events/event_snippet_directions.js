function activate_event_snippet_directions(){
	if (supports_geolocation()){
	    $(".event_list li .get_directions_link").each(function(i, el){
	        if ($(el).data("latitude") != "None" && $(el).data("longitude") != "None"){
	            $(el).show();
	        }
	    });
	}
}
$(document).ready(function(){
	activate_event_snippet_directions()
});