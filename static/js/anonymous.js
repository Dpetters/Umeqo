$(document).ready( function () {    
    $('.login_link').click(function(){
        $('#login_wrapper').fadeToggle('fast', function(){
            $('#id_username').focus();
        });
    });
    $(document).click(function(e) {
        if ($(e.target).parents('#login_wrapper').length == 0 && !$(e.target).hasClass("login_link")) {
            $('#login_wrapper').hide();
        }
    });
});