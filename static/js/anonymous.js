$('.login').live('click', function(e){
    $(".dialog").remove();
    $("#login_button a").click();
    e.preventDefault();
});

$(".resend_account_activation_email").live("click", function(e){
    document.resend_activation_email_form.submit();
    e.preventDefault();
});

$(document).ready( function () {
    $("#login_button a").click(function(e){
        $('#login_wrapper').fadeToggle('fast', function(){
            $('#id_username').focus();
        });
        e.preventDefault();
    });
    
    $(document).click(function(e) {
        if ($(e.target).parents('#login_wrapper').length == 0 && $(e.target).parents("#login_button").length==0 && !$(e.target).hasClass("login")) {
            $('#login_wrapper').hide();
            $("#login_button a").removeClass("um-pressed");
        }
    });
});
