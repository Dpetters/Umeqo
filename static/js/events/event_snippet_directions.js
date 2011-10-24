$(document).ready(function(){
    if (supports_geolocation()){
        $(".event_list li .get_directions_link").each(function(i, el){
            if ($(el).data("latitude") != "None" && $(el).data("longitude") != "None"){
                $(el).show();
            }
        });
    }
});