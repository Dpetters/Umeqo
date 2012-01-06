function update_checkin_count(){
    $.ajax({
        url: EVENT_CHECKIN_COUNT_URL,
        dataType: "json",
        data: {
            'event_id': EVENT_ID
        },
        success: function (data) {
            $("#event_checkin_count_num").html(data.count);
        },
        error: errors_in_message_area_handler
    });
}
$(document).ready(function() {
    if (typeof(google)!= "undefined"){
	    if (EVENT_LATITUDE && EVENT_LONGITUDE){
	        if (supports_geolocation()){
	            $(".get_directions_link").show();
	        }
	        $("#event_where #map").width(260).height(260).css("margin-top", "9px");
	        
	        var location = new google.maps.LatLng(EVENT_LATITUDE, EVENT_LONGITUDE);
	        var map_options = {
	          zoom: 16,
	          center: location,
	          mapTypeId: google.maps.MapTypeId.ROADMAP
	        };
	        var map = new google.maps.Map(document.getElementById("map"), map_options);
	        var marker = new google.maps.Marker({ map: map }); 
	        marker.setPosition(location);
	    }
    }else{
    	// No internet connection
    	$("#event_external_buttons").html("");
    }

    $('.event_rsvp').each(function() {
        $(this).click(function() {
            var id = $(this).attr('id');
            $('#f-' + id).submit();
        });
    });
    
    $('#event_tabs h2').each(function(i) {
        $(this).click(function() {
            $('.responses').addClass('hid');
            $('.responses').eq(i).removeClass('hid');
            $('.current').removeClass('current');
            $(this).addClass('current');
        });
    });

    if (window.location.hash == '#checkin') {
        var i = 1;
        $('.responses').addClass('hid');
        $('.responses').eq(i).removeClass('hid');
        $('.current').removeClass('current');
        $('#event_tabs h2').eq(i).addClass('current');
    }

    $('#email_input, #name_input').placeholder();

    // Used to move cursor to beginning of field.
    function setSelectionRange(input, selectionStart, selectionEnd) {
        if (input.setSelectionRange) {
            input.focus();
            input.setSelectionRange(selectionStart, selectionEnd);
        }
        else if (input.createTextRange) {
            var range = input.createTextRange();
            range.collapse(true);
            range.moveEnd('character', selectionEnd);
            range.moveStart('character', selectionStart);
            range.select();
        }
    }
    $('#email_input').mouseup(function(e) {
        var text_value = $.trim($(this).val());
        var email_suffix = '@mit.edu';
        if (text_value == '' || text_value == email_suffix) {
            if (this.value != email_suffix) {
                this.value = email_suffix;
            }
            if (this.setSelectionRange) {
                this.setSelectionRange(0, 0);
                this.focus();
            }
            else if (this.createTextRange) {
                var range = this.createTextRange();
                range.collapse(true);
                range.moveEnd('character', 0);
                range.moveStart('character', 0);
                range.select();
                this.focus();
            }
        }
    });
    $("#get_raffle_winner_link").live('click', function(){
        $.ajax({
            data:{'event_id':EVENT_ID},
            url:EVENT_RAFFLE_WINNER_URL,
            success: function(data) {
                if(data.name){
                    alert(data.name);
                }else{
                    alert("You ran out of attendees!");
                }
            },
            error: errors_in_message_area_handler
        });
    });
});