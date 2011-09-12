$(document).ready(function() {
    var xhr, map, geocodes, marker, map_options, mit_location;

    if ( typeof (google) !== "undefined") {
        mit_location = new google.maps.LatLng(42.35967402, -71.09201372);
        map_options = {
            zoom: 14,
            center: mit_location,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            streetViewControl: false,
            mapTypeControl: false
        };
        map = new google.maps.Map(document.getElementById("map"), map_options);
        

        function center_map_coord(latitude, longitude) {
            var location = new google.maps.LatLng(latitude, longitude);
            map.setCenter(location);
            map.setZoom(16);
            if ( typeof (marker) === "undefined" || !marker) {
                marker = new google.maps.Marker({
                    map: map
                });
            }
            marker.setPosition(location)
        }
        if (typeof(LATITUDE)!="undefined" && typeof(LONGITUDE)!="undefined"){
            center_map_coord(LATITUDE, LONGITUDE);
        }
        $(".location_suggestion").live('click', function() {
            $(".location_suggestion").removeClass("selected");
            $(this).addClass("selected");
            $("#id_location").val($(this).text());
            center_map_coord($(this).attr("data-latitude"), $(this).attr("data-longitude"));
        });
        
        function get_location_suggestions() {
            if ( typeof (marker) !== "undefined" && marker) {
                marker.setMap(null);
                marker = null;
            }
            if (xhr) {
                xhr.abort();
            }
            if ($('#id_location').val() != "") {
                query = $("#id_location").val();
                xhr = $.ajax({
                    type: 'GET',
                    url: GET_LOCATION_SUGGESTIONS_URL,
                    dataType: "html",
                    data: {
                        'query': query,
                    },
                    success: function(data) {
                        if (data) {
                            $("#location_suggestions").html(data);
                        } else {
                            if ( typeof (geocoder) === "undefined") {
                                geocoder = new google.maps.Geocoder();
                            }
                            var geocoderRequest = {
                                address: query,
                                location: mit_location,
                                region: "US"
                            }
                            geocoder.geocode(geocoderRequest, function(results, status) {
                                if (status == google.maps.GeocoderStatus.OK) {
                                    var html = "";
                                    $.each(
                                        results.slice(0, 8),
                                        function(i, l){
                                            var display_name = l.formatted_address;
                                            var lat = l.geometry.location.lat();
                                            var lng = l.geometry.location.lng();
                                            html += "<p class='location_suggestion' data-latitude='" + lat + "' data-longitude='" + lng + "'>" + display_name + "</p>"; 
                                        }
                                    )
                                    $("#location_suggestions").html(html);
                                }
                            });
                        }
                    },
                    error: errors_in_message_area_handler
                });
            } else {
                $("#location_suggestions").html("");
            }
        };
        
        $(".location_suggestion").live("keydown", function(e){
            if (e.which==13){
                $(this).click();
            } 
        });
        
        var timeoutID;
        $('#id_location').keydown(function(e) {
            var current = null;
            var next = null;
            if (e.which==37 || e.which==39){
                return false;
            }
            if (e.which==40){
                if ($(".selected").length > 0){
                    current = $($(".selected").get(0));
                    current.removeClass("selected");
                    next = current.next();
                    if (next.length > 0){
                        next.addClass("selected");
                    } else {
                        $($("#location_suggestions .location_suggestion").get(0)).addClass("selected");
                    }
                }
                else {
                    $($("#location_suggestions .location_suggestion").get(0)).addClass("selected");
                }
                e.preventDefault();
            } else if (e.which==38){
                if ($(".selected").length > 0){
                    current = $($(".selected").get(0));
                    current.removeClass("selected");
                    prev = current.prev();
                    if (prev.length > 0){
                        prev.addClass("selected");  
                    } else {
                        $($("#location_suggestions .location_suggestion").last().get(0)).addClass("selected");
                    }
                }
                else {
                    $($("#location_suggestions .location_suggestion").last().get(0)).addClass("selected");
                }
                e.preventDefault();
            } else if (e.which==13){
                if ($(".selected").length > 0){
                    $($(".selected").get(0)).click();
                } else {
                    var suggestions = $("#location_suggestions .location_suggestion");
                    if (suggestions.length >= 0){
                        $(suggestions.get(0)).click();
                    }   
                }
                e.preventDefault();
            }
            else if (e.which != 9 && e.which != 32) {
                if ( typeof timeoutID != 'undefined')
                    window.clearTimeout(timeoutID);
                timeoutID = window.setTimeout(get_location_suggestions, 50);
            }
        });
    }

    var event_rules = {
        name: {
            required: true
        },
        start_datetime_0: {
            required: {
                depends: function(element) {
                    var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline";
                }
            },
        },
        start_datetime_1: {
            required: {
                depends: function(element) {
                    var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline";
                }
            },
        },
        end_datetime_0: {
            required: {
                depends: function(element) {
                    var event_type = $("#id_type option:selected").text();
                    return event_type != "Rolling Deadline";
                }
            },
        },
        end_datetime_1: {
            required: {
                depends: function(element) {
                    var event_type = $("#id_type option:selected").text();
                    return event_type != "Rolling Deadline";
                }
            },
        },
        attending_employers: {
            required: {
                depends: function(element) {
                    return CAMPUS_ORG_EVENT;
                }
            }
        },
        description: {
            required: true,
        },
        type: {
            required: true,
        },
        location: {
            required: {
                depends: function(element) {
                    var event_type = $("#id_type option:selected").text();
                    return event_type != "Hard Deadline" || event_type != "Rolling Deadline";
                }
            },
        }
    };

    var messages = {
        name: {
            required : "Name is required.",
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
        },
        attending_employers: {
            required: "This field is required."
        }
    }
    
    $("#id_type").change(function() {
        var title = null;
        var button_text = null;
        var event_type = $("#id_type option:selected").text()
        if (event_type === "Hard Deadline" || event_type === "Rolling Deadline") {
            $($('label[for=id_start_datetime_0]').removeClass('required').children()[0]).remove();
            $("#event_location_section").slideUp()
            $("#event_location_section input").attr('disabled', 'disabled');
            $("#event_form input[type=submit]").val("Create Deadline");
            if (event_type === "Rolling Deadline") {
                if (EDIT_FORM){
                    title = "Edit Rolling Deadline"
                } else {
                    title = "New Rolling Deadline"
                }
                $("#event_form_header").html(title);
                $("#id_name").attr("placeholder", "Enter rolling deadline name");
                
                $("#event_datetime_block").slideUp();
            
                $($('label[for=id_end_datetime_0]').removeClass('required').children()[0]).hide();
                
                $("#start_datetime_wrapper select, #start_datetime_wrapper input, #end_datetime_wrapper select, #end_datetime_wrapper input").attr('disabled', 'disabled');
            } else if (event_type === "Hard Deadline") {
                if (EDIT_FORM){
                    title = "New Hard Deadline"
                } else {
                    title = "Edit Hard Deadline"
                }
                $("#event_datetime_block").slideDown();
                $("#event_form_header").html(title);
                $("#id_name").attr("placeholder", "Enter hard deadline name");
                
                            
                $("#end_datetime_wrapper").slideDown();
                $('label[for=id_end_datetime_0]').addClass('required');
                if ($('label[for=id_end_datetime_0] span.error').length > 0){
                    $('label[for=id_end_datetime_0] span.error').show();                
                } else {
                    $('label[for=id_end_datetime_0]').append("<span class='error'>*</span>");
                }     
                $("#start_datetime_wrapper select, #start_datetime_wrapper input").attr('disabled', 'disabled');
                $("#end_datetime_wrapper select, #end_datetime_wrapper input").removeAttr('disabled');
                $("#start_datetime_wrapper, #event_scheduler_day, #event_scheduler").slideUp();
            }
        } else {
            $('label[for=id_start_datetime_0]').addClass('required');
            if (EDIT_FORM){
                title = "Edit Event"
            } else {
                title = "New Event"
            }
            $("#event_form_header").html(title);
            $("#event_datetime_block").slideDown();
            if ($('label[for=id_start_datetime_0] span.error').length > 0){
                $('label[for=id_start_datetime_0] span.error').show();                
            } else {
                $('label[for=id_start_datetime_0]').append("<span class='error'>*</span>");                
            }
            
            $('label[for=id_end_datetime_0]').addClass('required');
            if ($('label[for=id_end_datetime_0] span.error').length > 0){
                $('label[for=id_end_datetime_0] span.error').show();                
            } else {
                $('label[for=id_end_datetime_0]').append("<span class='error'>*</span>");                
            }
            $("#start_datetime_wrapper select, #start_datetime_wrapper input, #end_datetime_wrapper select, #end_datetime_wrapper input").removeAttr('disabled');
            $("#start_datetime_wrapper, #end_datetime_wrapper, #event_scheduler_day, #event_scheduler").slideDown();
            $("#event_form input[type=submit]").val("Create Event");

            $("#event_location_section input").removeAttr('disabled');
            $("#event_location_section").slideDown();
        }
        if (EDIT_FORM){
            $("#event_form input[type=submit]").val("Save Changes");
        }
    });

    $('#id_type').change();

    $("#event_form").submit(function() {
        for (instance in CKEDITOR.instances)
            CKEDITOR.instances[instance].updateElement();
        if (marker && marker.map) {
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

    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 200,
        height: 146
    });

    if (CAMPUS_ORG_EVENT){
        $("#id_attending_employers").multiselect({
            noneSelectedText: 'select employers',
            classes: 'attending_employers_multiselect',
            minWidth: 310,
            height: 210,
            click: function(e, ui) {
                if (ui.checked){
                    $.ajax({
                        type: 'GET',
                        url: EMPLOYER_DETAILS_URL,
                        dataType: "html",
                        data: {
                            'employer_name':ui.text,
                        },
                        success: function (data) {
                            $("#attending_employers").append(data);
                        },
                        error: errors_in_message_area_handler
                    });
                } else {
                    $(".attending_employer[data-employer-name='" + ui.text + "']").remove();
                }
            },
            uncheckAll: function(){
                $("#attending_employers").html("");
            }
        }).multiselectfilter();
    }
    
    $('.datefield').datepicker({
        minDate: 0
    });
    // Fix validation bug
    $(".attending_employers_multiselect").blur(function(){
        if ($("#id_attending_employers").val()){
            event_form_validator.element("#id_attending_employers");
        }
    });
    // Prevent end datetime from being before start datetime.
    function getStartDate() {
        var start_date = $('#id_start_datetime_0').val().split('/');
        var month = start_date[0];
        var day = start_date[1];
        var year = start_date[2];
        var start_time = $('#id_start_datetime_1').val().split(':');
        var hour = start_time[0];
        var minute = start_time[1];
        var start = new Date(year, month-1, day, hour, minute, 0);
        return start;
    }

    function getEndDate() {
        var end_date = $('#id_end_datetime_0').val().split('/');
        var month = end_date[0];
        var day = end_date[1];
        var year = end_date[2];
        var end_time = $('#id_end_datetime_1').val().split(':');
        var hour = end_time[0];
        var minute = end_time[1];
        var end = new Date(year, month-1, day, hour, minute, 0);
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
    $('#id_start_datetime_0, #id_end_datetime_0').each(function() {
        $(this).data('prevValue', $(this).val());
    });
    $('#id_start_datetime_0').change(function() {
        if ($(this).val() == "") {
            $(this).val($(this).data('prevValue'));
        } else {
            var parts = $(this).val().split('/');
            var day = parts[1];
            var month = parts[0];
            var year = parts[2];
            var start_date = new Date(year, month-1, day, 0, 0, 0, 0);
            var now_date = removeTime(new Date());
            if (start_date - now_date < 0) {
                $(this).val($(this).data('prevValue'));
                $('#event_scheduler_day_text').val($(this).data('prevValue'));
            } else {
                $(this).data('prevValue', $(this).val());
            }
        }
    });
    $('#id_end_datetime_0').change(function() {
        if ($(this).val() == "") {
            $(this).val($(this).data('prevValue'));
        } else {
            $(this).data('prevValue', $(this).val());
        }
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
        var start_hour = start.getHours() + start.getMinutes() / 60;
        var start_px = 1 + 32 * start_hour;

        var start_date = removeTime(start);
        var end = getEndDate();
        var end_date = removeTime(end);
        var end_hour = end.getHours() + end.getMinutes() / 60;
        var end_px = 1 + 32 * end_hour;

        return {
            'start_date': start_date,
            'end_date': end_date,
            'name': name,
            'top': start_px,
            'bottom': end_px
        };
    }

    function getSchedulerDate() {
        var schedule_date_parts = $('#event_scheduler_day_text').val().split('/');
        var month = schedule_date_parts[0];
        var day = schedule_date_parts[1];
        var year = schedule_date_parts[2];
        // Months are 0-indexed!
        var schedule_date = new Date(year, month-1, day, 0, 0, 0, 0);
        return schedule_date;
    }

    function setEventDate(datetime) {
        setDate(datetime, 'event_scheduler_day_text');
    }

    function renderScheduler() {
        $('#event_scheduler_nav_back').removeClass('enabled');
        $('#event_scheduler_nav_forward').removeClass('enabled');
        var event_date_text = $('#event_scheduler_day_text').val();
        $('.event_block').remove();
        var get_data = {
            'event_date': event_date_text,
        };
        if (EDIT_FORM) {
            get_data['event_id'] = EVENT_ID;
        } else {
            get_data['event_id'] = 0;
        }
        if (event_date_text){
            $.get(EVENT_SCHEDULE_URL, get_data, function(res) {
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
                    height = (1 + 32 * 24) - top;
                    clipBottom = true;
                    // If event ends on displayed schedule, end at proper place.
                } else if (end_date - schedule_date == 0) {
                    height = thisEventInfo.bottom - top;
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
                $('#event_scheduler_nav_back').addClass('enabled');
                $('#event_scheduler_nav_forward').addClass('enabled');
            });
        }
    }

    $('#event_scheduler_day_text').datepicker({'minDate': null});
    $('#id_name, #id_start_datetime_0, #id_start_datetime_1, #id_end_datetime_0, #id_end_datetime_1, #event_scheduler_day_text').change(renderScheduler);
    renderScheduler();

    $('#event_scheduler_nav_back').click(function(e) {
        if ($(this).hasClass('enabled')) {
            var date = getSchedulerDate();
            date.setDate(date.getDate() - 1);
            setEventDate(date);
            renderScheduler();
        }
        e.preventDefault();
    });
    $('#event_scheduler_nav_forward').click(function(e) {
        if ($(this).hasClass('enabled')) {
            var date = getSchedulerDate();
            date.setDate(date.getDate() + 1);
            setEventDate(date);
            renderScheduler();
        }
        e.preventDefault();
    });
});
