$(document).ready( function () {    
    //toggle login form
    $('#login_button').click(function(){
        $('#login_wrapper').fadeToggle('fast',function(){
            $('#id_username').focus();
        });
    });
    $('#login_wrapper').hide();
    $(document).click(function(e) {
        if ($(e.target).parents('#login_wrapper').length == 0 &&
            $(e.target).parent().attr('id') != 'login_button') {
            $('#login_wrapper').hide();
        }
    });
});
