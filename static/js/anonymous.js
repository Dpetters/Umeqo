$(document).ready( function () {
	$("#login_button a").click(function(e){
		$('#login_wrapper').fadeToggle('fast', function(){
            $('#id_username').focus();
        });
        e.preventDefault();
	});
	
    $('.login').click(function(e){
    	$("#login_button a").click();
        e.preventDefault();
    });
    
    $(document).click(function(e) {
        if ($(e.target).parents('#login_wrapper').length == 0 && $(e.target).parents("#login_button").length==0 && !$(e.target).hasClass("login")) {
            $('#login_wrapper').hide();
            $("#login_button a").removeClass("um-pressed");
        }
    });
});
