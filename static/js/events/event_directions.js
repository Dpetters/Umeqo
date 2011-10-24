$(".get_directions_link").live('click', function(e){
    console.log("clicked");
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