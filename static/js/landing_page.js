$(document).ready(function() {
    $('input').focus(function() {
        var p = $(this).parents('.module');
        p.css("background","none");
        p.css("-ms-filter", "progid:DXImageTransform.Microsoft.gradient(startColorstr=#22ffffff,endColorstr=#22ffffff)");
        p.css("filter", "progid:DXImageTransform.Microsoft.gradient(startColorstr=#22ffffff,endColorstr=#22ffffff)");
        p.css("zoom", 1);
        p.css('background-color','rgba(255,255,255,0.2)');
    });
    $('input').blur(function() {
        var p = $(this).parents('.module');
        p.css("background", "auto");
        p.css("-ms-filter", "auto");
        p.css("filter", "auto");
        p.css("zoom", "auto");
        p.css('background-color','rgba(255,255,255,0.1)');
    });
});