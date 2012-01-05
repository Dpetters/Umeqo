var subscribe_to_employer_mouseout = false;

function subscribe_to_employer(subscribe){
    var that = this;
    var loaded_employer_id = $("#loaded_employer_id").val();
    $.ajax({
    	url:SUBSCRIBE_URL,
    	type:"POST",
    	data:{id: loaded_employer_id},
    	beforeSend: function(){
    		$(that).html("processing...");
	    	$("#subscribe, #unsubscribe").live('mouseout', function(){
				subscribe_to_employer_mouseout = true;
			});
    		$("#unsubsribe, #subscribe").live('mouseover', function(){
				subscribe_to_employer_mouseout = false;
			});
    	},
    	success: function(data) {
			if(subscribe){
				$(".employer_id[value=" + loaded_employer_id + "]").parent().addClass("subscribed");
				$(that).addClass("subscribed").attr("id", "unsubscribe");
				if(subscribe_to_employer_mouseout){
					$(that).html("Subscribed");
				}else{
					$(that).html("RSVP Unsubscribe");	
				}
			}else{
				$(".employer_id[value=" + loaded_employer_id + "]").parent().removeClass("subscribed");
				$(that).removeClass("subscribed").attr("id", "subscribe").html("Subscribe");
			}
    	},
        error: errors_in_message_area_handler
    });
}
$('#unsubscribe').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
		subscribe_to_employer.apply(this, [false]);
	}
    e.preventDefault();
});

$('#subscribe').live('click', function(e) {
	var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
		subscribe_to_employer.apply(this, [true]);
	}
    e.preventDefault();
});


$("#logo_and_buttons .subscribed").live('mouseenter', function(){
	$(this).html("Unsubscribe");
});
$("#logo_and_buttons .subscribed").live('mouseleave', function(){
	$(this).html("Subscribed");
});

function bindLoadEmployerHandlers() {
    $('.employer_snippet').each(function() {
        $(this).click(function() {
            var id = $(this).children('.employer_id').eq(0).val();
            loadEmployer(this, getID(this));
        });
    });
}
function getID(el) {
    return $(el).children('.employer_id').eq(0).val();
}

function loadEmployer(target, id, noPush) {
    var disablePush = noPush || false;
    var listing;
    if (!target) {
        $('.employer_snippet').each(function() {
            if (getID(this) == id) {
                listing = this;
            }
        })
    } else {
        listing = target;
    }
    show_form_submit_loader("#employers_form");
    $.get(EMPLOYER_DETAILS_URL, {id: id}, function(data) {
        $('#employer_details').html(data);
        if (!disablePush) {
            var stateObj = {id: id};
            history.pushState(stateObj, "employer "+id, EMPLOYERS_URL+"?id="+id);
        }
        $('.selected').removeClass('selected');
        $(listing).addClass('selected');
        hide_form_submit_loader("#employers_form");
    });
}

window.onpopstate = function(event) {
	console.log("onpopstate");
    if (event.state != null) {
        loadEmployer(null, event.state.id, true);
    } else if ($('#isnotajax').val()=='false') {
        loadEmployer(null, FIRST_EMPLOYER_ID, true);
    }
}

$(document).ready(function() {

    bindLoadEmployerHandlers();

    $('#employers_filter_name').keydown(function() {
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(filterEmployers,200);
    });

    $('#employers_filter_industry, #employers_filter_has_events, #employers_filter_in_subscriptions').change(function() {
        filterEmployers();
    });

    function filterEmployers() {
        var query = $('#employers_filter_name').val();
        var industry = $('#employers_filter_industry').val();
        var has_public_events_deadlines = $('#employers_filter_has_events').attr('checked')=="checked";
        var subscribed = $('#employers_filter_in_subscriptions').attr('checked')=="checked";
        show_form_submit_loader("#employers_form");
        $.ajax({
        	url:SEARCH_URL,
        	data:{
            	'q': query,
            	'i': industry,
            	'has_public_events_deadlines': has_public_events_deadlines,
            	'subscribed': subscribed
        	},
        	success:function(data) {
	            $('#employer_snippets').html(data);
	            bindLoadEmployerHandlers();
	            hide_form_submit_loader("#employers_form");
        	},
        	error:errors_in_message_area_handler,
        });
    }
});