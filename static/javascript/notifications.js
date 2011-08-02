$(document).ready(function() {
    var noticeid = window.location.hash.substring(1);
    $('#n-' + noticeid).effect('highlight', {}, 3000);
});