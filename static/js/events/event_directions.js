function activate_geolocation(){
    $('.location').replaceWith(function() {
        var latitude = $(this).data("latitude");
        var longitude = $(this).data("longitude");
        if (latitude != "None" && longitude != "None"){
            var url = $.trim($(this).text());
            return '<a class="get_directions" data-longitude="' + longitude + '" data-latitude="' + latitude + '" href="' + url + '" target="_blank">' + url + '</a>';            
        }
        return $(this).contents();
    });
}

$(".get_directions").live('click', function(e){
    var that = this;
    function getDirections(position){
        slat = position.coords.latitude;
        slng = position.coords.longitude;
        elat = $(that).data("latitude");
        elng = $(that).data("longitude");
        window.location = "http://maps.google.com/?dirflg=r&saddr=" + slat + "," + slng + "&daddr=" + elat + "," +  elng;
    }
    navigator.geolocation.getCurrentPosition(getDirections);
    e.preventDefault();
});

$(document).ready(function(){
    if (supports_geolocation()){
        activate_geolocation();
    }
});