$(document).ready(function(){
	if (window.location.pathname == HELP_CENTER_URL){
		$("#help_center_link").css('background', "#FFF");
	}
	else if (window.location.pathname == FAQ_URL){
		$("#faq_link").css('background', "#FFF");		
	}
	else if (window.location.pathname == TUTORIALS_URL){
		$("#tutorials_link").css('background', "#FFF");
	}
});
