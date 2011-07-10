$(document).ready( function () {
    
    //toggle show/hide login form
    $('#login_button').click(function(){
        $('#loginWrapper').fadeToggle('fast',function(){
            $('#id_username').focus();
        });
    });
    $('#loginWrapper').hide();
    $(document).click(function(e) {
        if ($(e.target).parents('#loginWrapper').length == 0 &&
            $(e.target).parent().attr('id') != 'login_button') {
            $('#loginWrapper').hide();
        }
    });
});
