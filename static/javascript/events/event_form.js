$(document).ready( function() {
	var xhr, map, geocodes, marker, map_options, mit_location;
	
	if (typeof(google) !== "undefined"){
		mit_location = new google.maps.LatLng(42.35967402, -71.09201372);
	    
	    map_options = {
	      zoom: 14,
	      center: mit_location,
	      mapTypeId: google.maps.MapTypeId.ROADMAP,
	      streetViewControl:false,
	      mapTypeControl:false
	      
	    };
		map = new google.maps.Map(document.getElementById("map"), map_options);
	
		function center_map_coord(latitude, longitude){
			var location = new google.maps.LatLng(latitude, longitude);
		    map.setCenter(location)
		    map.setZoom(16);
	        if (typeof(marker)==="undefined") {
	        	marker = new google.maps.Marker({ 
	        		map: map
	         	});
			}
			marker.setPosition(location)
	  	}
	
	  	function center_map_address(address){
	        if (typeof(geocoder)==="undefined"){
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
	                if (typeof(marker)==="undefined") {
	                	marker = new google.maps.Marker({ 
	                		map: map
	                 	}); 
					}
	    			marker.setPosition(results[0].geometry.location)
		  		}
		  	});
		};
		
		$(".location_suggestion").live('click', function(){
			$(".location_suggestion").removeClass("selected");
			$(this).addClass("selected");
			$("#id_location").val($(this).text());
			center_map_coord($(this).attr("data-latitude"), $(this).attr("data-longitude")); 
		});
	    
	    function get_location_guess(){
	    	if (typeof(marker) !== "undefined" && marker){
	    		marker.setMap(null);
	    		marker = null;
	    	}
	    	if (xhr){
	    		xhr.abort();
	    		$("#location_suggestions").html("");
	    	}
	    	if ($('#id_location').val() != ""){
				xhr = $.ajax({
		            type: 'GET',
		            url: GET_LOCATION_GUESS_URL,
		            dataType: "json",
		            data: {
		                'query': $("#id_location").val(),
		            },
		            beforeSend: function(jqXHR, settings){
		            	$("#location_suggestions").html(MEDIUM_AJAX_LOADER);
		            },
		            success: function (data) {
		            	console.log(data);
		            	var query = $("#id_location").val();
		                if (data.valid){
		                	center_map_coord(data.latitude, data.longitude);
		                	$("#location_suggestions").html("");
		                }else{
		                	xhr = $.ajax({
					            type: 'GET',
					            url: GET_LOCATION_SUGGESTIONS_URL,
					            dataType: "html",
					            data: {
					                'query': query,
					            },
					            success: function (data) {
					            	if(data){
					                	$("#location_suggestions").html(data);
					            	} else {
					            		$("#location_suggestions").html("");
					            		center_map_address(query);
					            	}
					            },
					        });
		                }
		            },
		            error: function(jqXHR, textStatus, errorThrown) {
		            	if (errorThrown != "abort")
		            	{
			                if(jqXHR.status==0){
			                    show_error_dialog(page_check_connection_message);
			                }else{
			                    show_error_dialog(page_error_message);
			                }
		                }
		            }
		        });
		     } else {
		     	$("#location_suggestions").html("");
		     }
	    }
	    
	    var timeoutID;
	    $('#id_location').keydown( function(e) {
	    	if(e.which != 9){
		        if (typeof timeoutID!='undefined')
		            window.clearTimeout(timeoutID);
		        timeoutID = window.setTimeout(get_location_guess, 100);
	       }
	    });
	}

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
        description:{
        	required:true,
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
        	$("#event_form_header").html("New Deadline");
        	
        	$("#id_name").attr("placeholder", "Enter deadline name");
			
        	$("#event_location_section").css("opacity", .2);
        	$("#event_location_section input").attr('disabled', 'disabled');
	        
	        if(event_type === "Rolling Deadline") {
	        	$("#event_datetime_block").css("opacity", .2);
	        	$("#start_datetime_wrapper select, #start_datetime_wrapper input").attr('disabled', 'disabled');
	        } else if(event_type === "Hard Deadline"){
	      		$("#event_datetime_block").css("opacity", 1);
	        	$("#start_datetime_wrapper select, #start_datetime_wrapper input").removeAttr('disabled');
	      		$("#start_datetime_wrapper").css("opacity", .2);
	        	$("#start_datetime_wrapper select, #start_datetime_wrapper input").attr('disabled', 'disabled');
	        	//$("#id_start_datetime_0").bind('hover', cursor_display);
	        }
        } else {
        	$("#event_form_header").html("New Event");
        	//$("#id_start_datetime_0").unbind('hover', cursor_display);
        	$("#start_datetime_wrapper select, #start_datetime_wrapper input").removeAttr('disabled');
        	$("#start_datetime_wrapper").css("opacity", 1);
        	
        	$("#event_location_section input").removeAttr('disabled');
        	$("#event_location_section").css("opacity", 1);
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
    
	$("#event_form").submit(function(){
		if (marker && marker.map){
			$("#id_latitude").val(marker.position.lat());
			$("#id_longitude").val(marker.position.lng());			
		}
	});
	
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
                    if(jqXHR.status==0){
	                    show_error_dialog(page_check_connection_message);
                    }else{
	                    show_error_dialog(page_error_message);
	                }
                }
            }
        });
    }
	console.log("hi");
    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 200,
        height:146
    });
    
    $('label[for=id_start_datetime_0]').addClass('required');
    
    $('.datefield').datepicker({
        minDate: 0
    });
});
