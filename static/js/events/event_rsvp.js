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

function rsvp(isAttending) {
    $.ajax({
    	url:$(this).attr('href'),
    	data:{ isAttending: isAttending },
    	success: function(data) {
        	if ($('.response').length > 0) {
            	$('.no-response').removeClass('hid');
            	$('.response').addClass('hid');
        	} else {
            	$('.no-response').removeClass('hid');
        	}
    	},
    	error: errors_in_message_area_handler
    });
    
    if (isAttending) {
        $("#event_resume_drop").click();
    }
}

$('#rsvp-yes-button').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!$(this).hasClass('selected') && (typeof disabled == 'undefined' || disabled !== true)) {
        rsvp.apply(this, [true]);
        $('#rsvp_div .selected').removeClass('selected');
        $(this).addClass('selected');

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
    e.preventDefault();
});

$('#rsvp-no-button').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!$(this).hasClass('selected') && (typeof disabled == 'undefined' && disabled !== true)) {
    	rsvp.apply(this, [false]);
        $('#rsvp_div .selected').removeClass('selected');
        $(this).addClass('selected');
    }
    e.preventDefault();
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
        $("#rsvp-yes-button").click();
    }
    if (get_parameter_by_name("rsvp")=="false"){
        $("#rsvp-no-button").click();
    }
});