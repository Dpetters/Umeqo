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
        timeoutID = window.setTimeout(get_location_guess, 500);
    });

    var event_rules = {
        name:{
            required: true
        },
        start_datetime_0:{
            required: {
                depends: function(element) {
                	var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline" ;
                }
            },
        },
        start_datetime_1:{
            required: {
                depends: function(element) {
                	var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline" ;
                }
            },
        },
        end_datetime_0:{
            required: {
                depends: function(element) {
                	var event_type = $("#id_type option:selected").text();
                    return event_type != "Rolling Deadline" ;
            	}
            },
        },
        end_datetime_1:{
            required: {
                depends: function(element) {
                	var event_type = $("#id_type option:selected").text();
                    return event_type != "Rolling Deadline" ;
            	}
            },
        },
        type:{
            required:true,
        }, 
        location:{
            required: {
                depends: function(element) {
                	var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline" ;
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

    $("#id_type").change( function() {
    	var event_type = $("#id_type option:selected").text()
        if (event_type === "Hard Deadline" || event_type === "Rolling Deadline"){
        	$("#id_start_datetime_0").hover( function(){
        		 console.log("hi");
			     $(this).css('cursor', 'default');
			});
        	$("#id_name").attr("placeholder", "Enter deadline name");
        	$("#start_datetime_wrapper").css("opacity", .2);
        	$("#start_datetime_wrapper :input").attr('disabled', true);
        	$("#start_datetime_wrapper :select").attr('disabled', 'disabled');
        	$("#event_location_section").css("opacity", .2);
        	$("#start_location_section :input").attr('disabled', true);
        	$("#event_name_section .step").html("Step 1 - Pick Deadline Name (required)");
        	$("#event_description_section .step").html("Step 3 - Describe Event (required)");
        } else {
        	$("#start_datetime_wrapper").css("opacity", 1);
        	$("#event_location_section").css("opacity", 1);
        }
        if(event_type === "Rolling Deadline") {
        	$("#event_form_header").html("New Rolling Headline");
        	$("#event_datetime_block").css("opacity", .2);
        	$("#start_datetime_block :input").attr('disabled', true);
        } else{
            $("#event_datetime_block").css("opacity", 1); 
            $('#event_datetime_block :input').removeAttr('disabled');
        	if (event_type === "Hard Deadline") {
        		$("#event_datetime_block .main_block_header_title").html("Step 5 - Pick Date & Time (required)");
        		$("#event_form_header").html("New Hard Headline");
        	}
        }
    });

	var config = {
		toolbar:
		[
			['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink'],
			['UIColor']
		]
	};
    $("#id_description").ckeditor(config);
    
    $('#id_type').change();

    var event_form_validator = $("#event_form").validate({
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
                            $("#event_form_block .main_block_content").html(status_500_message);
                            break;
                        default:
                            $("#event_form_block .main_block_content").html(check_connection_message);    
                    }
                },
            }
        });
    }

    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 220,
        height:146
    });
    
    $('label[for=id_start_datetime_0]').addClass('required');
    
    $('.datefield').datepicker({
        minDate: 0
    });
});
