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
            if (typeof(marker)==="undefined" || !marker) {
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
                    if (typeof(marker)==="undefined" || !marker) {
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
            $('label[for=id_start_datetime_0]').removeClass('required');
    
            $("#event_form_header").html("New Deadline");
            
            $("#id_name").attr("placeholder", "Enter deadline name");
            
            $("#event_location_section").css("opacity", .2);
            $("#event_location_section input").attr('disabled', 'disabled');
            
            if (event_type === "Rolling Deadline") {
                $("#event_datetime_block").css("opacity", .2);
                $("#start_datetime_wrapper select, #start_datetime_wrapper input").attr('disabled', 'disabled');
            } else if(event_type === "Hard Deadline"){
                $("#event_datetime_block").css("opacity", 1);
                $("#start_datetime_wrapper select, #start_datetime_wrapper input").removeAttr('disabled');
                $("#start_datetime_wrapper").css("opacity", .2);
                $("#start_datetime_wrapper select, #start_datetime_wrapper input").attr('disabled', 'disabled');
            }
        } else {
            $('label[for=id_start_datetime_0]').addClass('required');
            $("#event_form_header").html("New Event");
            $("#start_datetime_wrapper select, #start_datetime_wrapper input").removeAttr('disabled');
            $("#start_datetime_wrapper").css("opacity", 1);
            
            $("#event_location_section input").removeAttr('disabled');
            $("#event_location_section").css("opacity", 1);
        }
    });

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
        errorPlacement: place_table_form_field_error,
        rules: event_rules,
        messages: messages
    });
    if (typeof EDIT_FORM != 'undefined' && EDIT_FORM==false) {
        $('#id_name').rules("add", {
            remote: {
                url: CHECK_NAME_AVAILABILITY_URL,
                error: function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.status==0) {
                        show_error_dialog(page_check_connection_message);
                    } else {
                        show_error_dialog(page_error_message);
                    }
                }
            }
        });
    }
    
    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 200,
        height:146
    });
    
    $('.datefield').datepicker({
        minDate: 0
    });
    
    // Prevent end datetime from being before start datetime.
    function getStartDate() {
        var start_date = $('#id_start_datetime_0').val().split('/');
        var start_time = $('#id_start_datetime_1').val();
        var start = new Date(start_date[2] + '-' + start_date[0] + '-' + start_date[1] + ' ' + start_time);
        return start;
    }
    function getEndDate() {
        var end_date = $('#id_end_datetime_0').val().split('/');
        var end_time = $('#id_end_datetime_1').val();
        var end = new Date(end_date[2] + '-' + end_date[0] + '-' + end_date[1] + ' ' + end_time);
        return end;
    }
    function setDate(datetime, field_id) {
        // Don't forget JavaScript months are 0-indexed.
        var month = datetime.getMonth() + 1;
        if (month < 10) {
            month = '0' + month;
        }
        var day = datetime.getDate();
        if (day < 10) {
            day = '0' + day;
        }
        var date = month + '/' + day + '/' + datetime.getFullYear();
        if ($('#' + field_id)[0].nodeName == 'SPAN') {
            $('#' + field_id).html(date);
        } else {
            $('#' + field_id).val(date);
        }
    }
    function setTime(datetime, field_id) {
        var hours = datetime.getHours();
        if (hours < 10) {
            hours = '0' + hours;
        }
        var minutes = datetime.getMinutes();
        if (minutes < 10) {
            minutes = '0' + minutes;
        }
        var time = hours + ':' + minutes;
        $('#' + field_id).val(time);
    }
    $('#id_start_datetime_0, #id_start_datetime_1').change(function() {
        var start = getStartDate();
        var end = getEndDate();
        if (end - start <= 0) {
            end = new Date(start);
            end.setHours(end.getHours() + 1);
        }
        setDate(end, 'id_end_datetime_0');
        setTime(end, 'id_end_datetime_1');
        syncSchedule();
    });
    $('#id_end_datetime_0, #id_end_datetime_1').change(function() {
        var start = getStartDate();
        var end = getEndDate();
        if (end - start <= 0) {
            start = new Date(end);
            start.setHours(start.getHours() - 1);
        }
        setDate(start, 'id_start_datetime_0');
        setTime(start, 'id_start_datetime_1');
        syncSchedule();
    });
    
    // Event scheduler.
    function syncSchedule() {
        $('#event_scheduler_day_text').val($('#id_start_datetime_0').val());
        renderScheduler();
    }
    function removeTime(datetime) {
        var date = new Date(datetime);
        date.setHours(0);
        date.setMinutes(0);
        date.setSeconds(0);
        date.setMilliseconds(0);
        return date;
    }
    function getCurrentEventItem() {
        var name = $('#id_name').val();
        
        var start = getStartDate();
        var start_hour = start.getHours() + start.getMinutes()/60;
        var start_px = 1 + 32*start_hour;
        
        var start_date = removeTime(start);
        var end = getEndDate();
        var end_date = removeTime(end);
        if (end_date > start_date) {
            var end_hour = 24;
        } else {
            var end_hour = end.getHours() + end.getMinutes()/60;
        }
        var end_px = 1 + 32*end_hour;
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'name': name,
            'top': start_px,
            'height': end_px - start_px
        };
    }
    function getSchedulerDate() {
        var schedule_date_parts = $('#event_scheduler_day_text').val().split('/');
        var schedule_date = new Date(schedule_date_parts[2] + '-' + schedule_date_parts[0] + '-' + schedule_date_parts[1]);
        return schedule_date;
    }
    function setEventDate(datetime) {
        setDate(datetime, 'event_scheduler_day_text');
    }
    function renderScheduler() {
        $('#event_scheduler_nav_back').removeClass('active');
        $('#event_scheduler_nav_forward').removeClass('active');
        var event_date_text = $('#event_scheduler_day_text').val();
        $('.event_block').remove();
        $.get(EVENT_SCHEDULE_URL, {
            event_date: event_date_text
        }, function(res) {
            var highest = Infinity;
            $.each(res, function(i, eventInfo) {
                var title = eventInfo[0];
                var top = eventInfo[1];
                var height = eventInfo[2];
                var newEvent = $('<div>' + title + '</div>').addClass('event_block').addClass('gray');
                newEvent.css('top', top).css('height', height - 8);
                $('#event_scheduler').append(newEvent);
                if (top < highest) {
                    highest = top;
                }
            });
            
            var thisEventInfo = getCurrentEventItem();
            
            var schedule_date = removeTime(getSchedulerDate());
            var start_date = thisEventInfo.start_date;
            var end_date = thisEventInfo.end_date;
            
            var clipTop = false;
            var clipBottom = false;
            //Defaults to Infinity.
            var top = Infinity;
            // If event starts before displayed schedule, start from top.
            if (start_date - schedule_date < 0) {
                top = 0;
                clipTop = true;
            // If event starts on displayed schedule, start from proper place.
            } else if (start_date - schedule_date == 0) {
                top = thisEventInfo.top;
            }
            
            //Height defaults to Infinity.
            var height = Infinity;
            // If event ends after displayed schedule, end at bottom.
            if (end_date - schedule_date > 0) {
                height = (1 + 32*24) - top;
                clipBottom = true;
            // If event ends on displayed schedule, end at proper place.
            } else if (end_date - schedule_date == 0) {
                height = thisEventInfo.height;
            }
            
            if (top != Infinity && height != Infinity) {
                var name = thisEventInfo.name;
                if (name == '') {
                    name = 'New Event';
                }
                var thisEvent = $('<div>' + name + '</div>').addClass('event_block').addClass('green');
                thisEvent.css('top', top).css('height', height - 8);
                if (clipTop) {
                    thisEvent.addClass('clipTop');
                }
                if (clipBottom) {
                    thisEvent.addClass('clipBottom');
                }
                $('#event_scheduler').append(thisEvent);
                thisEvent.click(function() {
                    $('#id_name').focus();
                });
                if (top < highest) {
                    highest = top;
                }
            }
            
            if (highest < Infinity) {
                $('#event_scheduler').scrollTop(highest - 32);
            } else {
                $('#event_scheduler').scrollTop(0);
            }
            $('#event_scheduler_nav_back').addClass('active');
            $('#event_scheduler_nav_forward').addClass('active');
        });
    }
    $('#event_scheduler_day_text').val($('#id_start_datetime_0').val()).datepicker();
    $('#id_name, #id_start_datetime_0, #id_start_datetime_1, #id_end_datetime_0, #id_end_datetime_1, #event_scheduler_day_text').change(renderScheduler);
    renderScheduler();
    
    $('#event_scheduler_nav_back').click(function(e) {
        if ($(this).hasClass('active')) {
            var date = getSchedulerDate();
            date.setDate(date.getDate() - 1);
            setEventDate(date);
            renderScheduler();
            e.preventDefault();
        }
    });
    $('#event_scheduler_nav_forward').click(function(e) {
        if ($(this).hasClass('active')) {
            var date = getSchedulerDate();
            date.setDate(date.getDate() + 1);
            setEventDate(date);
            renderScheduler();
            e.preventDefault();
        }
    });
});
