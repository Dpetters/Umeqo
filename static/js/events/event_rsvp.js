function open_rsvp_info_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"RSVP Message",
        dialogClass: "rsvp_info_dialog",
        modal:true,
        width:550,
        resizable: false,
        close: function() {
            rsvp_info_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function rsvp(attending) {
	var that = this;
    $.ajax({
        type:'POST',
    	url: RSVP_URL,
    	data:{ attending: attending },
    	beforeSend:function(){
    		$(that).html("processing...");
    	},
    	success: function(data) {
    		var $dropdown_button = $(that).parents(".dropdown_button");
    		if($dropdown_button){
    			$dropdown_button.removeClass("dropdown_button").addClass("gray_button");
    		}
			if(attending){
				$(that).removeClass("not_attending").addClass("attending").attr("id", "rsvp_not_attending").html("RSVP Not Attending");
			}else{
				$(that).removeClass("attending").addClass("not_attending").attr("id", "rsvp_attending").html("RSVP Attending");
			}
    	},
    	error: errors_in_message_area_handler
    });
    
    if (attending) {
        $("#drop_resume").click();
    }
}

function show_rsvp_message(){
    $.ajax({
        data:{'event_id':EVENT_ID},
        url:RSVP_MESSAGE_URL,
        success: function(data) {
            if(data){
                rsvp_info_dialog = open_rsvp_info_dialog();
                rsvp_info_dialog.html(data);
            }
        },
        error: errors_in_message_area_handler
    });
}

$(".attending").live('mouseenter', function(){
	$(this).html("RSVP Not Attending");
});
$(".attending").live('mouseleave', function(){
	$(this).html("Attending");
});

$(".not_attending").live('mouseenter', function(){
	$(this).html("RSVP Attending");
});
$(".not_attending").live('mouseleave', function(){
	$(this).html("Not Attending");
});

$('#rsvp_attending').live('click', function(e) {
    rsvp.apply(this, [true]);
});
$('#rsvp_not_attending').live('click', function(e) {
    rsvp.apply(this, [false]);
});

$('#remove-rsvp-button').live('click', function(e) {
    $.ajax({
    	url: $(this).attr('href'),
    	success:function(data) {
        	$('.response').removeClass('hid');
        	$('.no-response').addClass('hid');
        	$('#rsvp_div .selected').removeClass('selected');
       	},
    	error: errors_in_message_area_handler
    });
    e.preventDefault();
});
    
$(document).ready(function(){
	if (get_parameter_by_name("rsvp")=="true"){
        $("#rsvp_yes_button").click();
    }
    if (get_parameter_by_name("rsvp")=="false"){
        $("#rsvp-no-button").click();
    }
});