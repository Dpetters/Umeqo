$(document).ready( function() {
    var mit_location = new google.maps.LatLng(42.35967402, -71.09201372);
    var xhr, map, geocoder, marker;
    var map_options = {
      zoom: 14,
      center: mit_location,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
	map = new google.maps.Map(document.getElementById("map"), map_options);

	function center_map_coord(latitude, longitude){
		var location = new google.maps.LatLng(latitude, longitude);
	    map.setCenter(location)
	    map.setZoom(16);
        if (!marker) {
        	marker = new google.maps.Marker({ 
        		map: map
         	});
		}
		marker.setPosition(location)
  	}

  	function center_map_address(address){
        if (!geocoder){
 			geocoder = new google.maps.Geocoder();        
        }

        var geocoderRequest = {
        	address: address,
        	location: mit_location,
        	region: "US"
        }
        
  		geocoder.geocode(geocoderRequest, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                map.setZoom(16);
                if (!marker) {
                	marker = new google.maps.Marker({ 
                		map: map
                 	}); 
				}
    			marker.setPosition(results[0].geometry.location)
	  		}
	  	});
	};

    function get_location_guess(){
    	if (xhr){
    		xhr.abort();
    	}
		xhr = $.ajax({
            type: 'GET',
            url: GET_LOCATION_GUESS_URL,
            dataType: "json",
            data: {
                'query': $("#id_location").val(),
            },
            success: function (data) {
                if (data.valid){
                	center_map_coord(data.latitude, data.longitude);
                }else{
                	center_map_address(data.query);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    show_error_dialog(page_check_connection_message);
                }else{
                    show_error_dialog(page_error_message);
                }
            }
        });
    }
    
    var timeoutID;
    $('#id_location').keydown( function() {
        if (typeof timeoutID!='undefined')
            window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(get_location_guess, 1000);
    });
  
    var event_rules = {
        name:{
            required: true
        },
        start_datetime_0:{
            required: {
                depends: function(element) {
                    return $("#id_type option:selected").text() != "Deadline";
                }
            },
        },
        start_datetime_1:{
            required: {
                depends: function(element) {
                    return $("#id_type option:selected").text() != "Deadline";
                }
            },
        },
        end_datetime_0:{
            required: true,
        },
        end_datetime_1:{
            required: true,
        },
        type:{
            required:true,
        }, 
        location:{
            required:{
                depends: function(element) {
                    return $("#id_type option:selected").text() != "Deadline";
                }
            },
        }
    };
		
    var messages = {
        name: {
            required: "Name is required.",
            remote: "Event name already taken."
        },
        type: {
            required: 'Event type is required.'
        },
        start_datetime_0: {
            required: 'Start date and time are required.'
        }, 
        start_datetime_1: {
            required: 'Start date and time are required.'
        },
        end_datetime_0: {
            required: 'End date and time are required.'
        }, 
        end_datetime_1: {
            required: 'End date and time are required.'
        },
        location: {
            required: 'Location is required.'
        }
    }

    $("label[for=id_description]").css('padding-left', '0px');

    $("#id_type").change( function() {
        if($("#id_type option:selected").text() === "Deadline") {
            $("label[for=   ]").text("Deadline Name");
            $("label[for=id_description]").text("Deadline Description");
            $('.event_only_field').hide();
        } else {
            $('.event_only_field').each( function() {
                $(this).show();
            });
        }
    });
    
    $('#id_type').change();

    var event_form_validator = $("#new_event_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
        rules: event_rules,
        messages: messages
    });
    if (typeof EDIT_FORM != 'undefined' && EDIT_FORM==false) {
        $('#id_name').rules("add",{
            remote: {
                url: CHECK_NAME_AVAILABILITY_URL,
                error: function(jqXHR, textStatus, errorThrown) {
                    switch(jqXHR.status){
                        case 500:
                            $("#new_event_form_block .main_block_content").html(status_500_message);
                            break;
                        default:
                            $("#new_event_form_block .main_block_content").html(check_connection_message);    
                    }
                },
            }
        });
    }

    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 204,
        height:146
    });
    
    $('label[for=id_start_datetime_0]').addClass('required');
    
    $('.datefield').datepicker({
        minDate: 0
    });
});
