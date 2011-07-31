$(document).ready(function() {
    var noticeid = window.location.hash.substring(1);
    console.log(noticeid);
    $('#n-' + noticeid).effect('highlight', {}, 3000);
    console.log(window.location);
});