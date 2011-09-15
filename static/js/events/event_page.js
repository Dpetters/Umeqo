$(document).ready(function() {
    if (EVENT_LATITUDE && EVENT_LONGITUDE){
        if (supports_geolocation()){
            $(".get_directions_link").append('<a href="#">Get directions</a>');
            $(".get_directions_link a").live('click', function(e){
                function getDirections(position){
                    slat = position.coords.latitude;
                    slng = position.coords.longitude;
                    elat = EVENT_LATITUDE;
                    elng = EVENT_LONGITUDE;
                    window.location = "http://maps.google.com/?dirflg=r&saddr=" + slat + "," + slng + "&daddr=" + elat + "," +  elng;
                }
                navigator.geolocation.getCurrentPosition(getDirections);
                e.preventDefault();
            })
        }
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

    function rsvp(isAttending) {
        $.post($(this).attr('href'), {
            isAttending: isAttending
        }, function(data) {
            if (typeof data.valid != 'undefined' && data.valid == true) {
                if ($('.response').length > 0) {
                    $('.no-response').removeClass('hid');
                    $('.response').addClass('hid');
                } else {
                    $('.no-response').removeClass('hid');
                }
            }
        }, "json");
        if (isAttending) {
            dropResume();
        } else {
            undropResume();
        }
    }
    function dropResume() {
        $('#event_resume_drop').attr('id', 'event_resume_undrop');
        $('#event_resume_undrop').html('Undo Drop Resume');
    }
    function undropResume() {
        $('#event_resume_undrop').attr('id', 'event_resume_drop');
        $('#event_resume_drop').html('Drop Resume');
    }

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
    
    $('#rsvp-yes-button').live('click', function(e) {
        var disabled = $(this).attr('disabled');
        if ($(this).hasClass('selected') || typeof disabled !== 'undefined' && disabled !== false) {
            e.preventDefault();
            return;
        }
        rsvp.apply(this, [true]);
        if ($(this).hasClass('left-group')) {
            $('#rsvp_div .selected').removeClass('selected');
            $(this).addClass('selected');
            $("#remove-rsvp-button").text("Undo RSVP and Resume Drop");
        }
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
        e.preventDefault();
    });
    $('#rsvp-no-button').live('click', function(e) {
        var disabled = $(this).attr('disabled');
        if ($(this).hasClass('selected') || typeof disabled !== 'undefined' && disabled !== false) {
            e.preventDefault();
            return;
        }
        rsvp.apply(this, [false]);
        if ($(this).hasClass('right-group')) {
            $('#rsvp_div .selected').removeClass('selected');
            $(this).addClass('selected');
            $("#remove-rsvp-button").text("Undo RSVP");
        }
        e.preventDefault();
    });
    $('#remove-rsvp-button').live('click', function(e) {
        $.post($(this).attr('href'), function(data) {
            if (typeof data.valid != 'undefined' && data.valid == true) {
                $('.response').removeClass('hid');
                $('.no-response').addClass('hid');
                $('#rsvp_div .selected').removeClass('selected');
                undropResume();
            }
        }, "json");
        e.preventDefault();
    });
    $('.event_rsvp').each(function() {
        $(this).click(function() {
            var id = $(this).attr('id');
            $('#f-' + id).submit();
        });
    });
    function getEmail() {
        return $('#email_input').val();
    }
    function getName() {
        return $('#name_input').val();
    }
    var rsvps, selectedIndex = 0, userText = "";
    $('#event_checkin_link').click(function(e) {
        window.scroll(0,0);
        $(this).children('.filler').eq(0).animate({
            height: '100%'
        }, function() {
            $.ajax({
                url:EVENT_RSVP_URL,
                success: function(data) {
                    rsvps = data;
                    $.ajax({
                        url:CHECKIN_URL,
                        success: function(data) {
                            $('#checkins').children().remove();
                            $.each(data, function() {
                                var newLi = $('#checkins_li_template').clone();
                                newLi.children('.name').eq(0).html(this.name);
                                newLi.children('.email').eq(0).html(this.email);
                                newLi.attr('id','');
                                $('#checkins').append(newLi);
                            });
                            $('#event_checkin_main').removeClass('hid').animate({
                                opacity: 1.0
                            });
                            $('body').addClass('overflowHidden');
                        },
                        error: errors_in_message_area_handler
                    });
                },
                error: errors_in_message_area_handler
            });
        });
        $(this).addClass('filled');
        e.preventDefault();
    });
    $('#email_input').keydown(function(e) {
        if (e.which == 38) {
            e.preventDefault();
        }
    });
    function moveHighlight(direction) {
        if (direction == -1 && selectedIndex > 0) {
            selectedIndex -= 1;
        } else if (direction == 1 && selectedIndex < $('#email_input_autofill li').length) {
            selectedIndex += 1;
        }
        $('.selected').removeClass('selected');
        var selectedLi = $('#email_input_autofill li').eq(selectedIndex - 1);
        if (selectedIndex > 0) {
            selectedLi.addClass('selected');
            $('#email_input').val(selectedLi.html());
        } else {
            $('#email_input').val(userText);
        }
    }
    function clearMatches() {
        $('#email_input_autofill').empty();
        selectedIndex = 0;
    }
    function findRSVPMatches(ref_email) {
        clearMatches();
        var i, rsvp;
        for (i = 0; i < rsvps.length; i += 1) {
            rsvp = rsvps[i];
            if (rsvp.email.indexOf(ref_email) === 0 && $('#email_input_autofill li').length < 5) {
                $('#email_input_autofill').append($('<li>' + rsvp.email + '</li>'));
            }
        }
    }
    $('#email_input').keyup(function(e) {
        var email = getEmail();
        //down button
        if (e.which == 40) {
            moveHighlight(1);
        //up button
        } else if (e.which == 38) {
            moveHighlight(-1);
        //otherwise...
        } else if (email.length > 1) {
            userText = email;
            var matches = findRSVPMatches(email);
        } else {
            clearMatches();
        }
    });
    $('#checkin_form input').each(function() {
        $(this).keyup(function(e) {
            //enable submit by enter button
            if (e.which == 13) {
                clearMatches();
                $(this).closest('form').submit();
            } else {
                hideError();
                $('#checkin_status').removeClass();
            }
        });
    });
    $('#email_input_autofill li').live('click', function() {
        clearMatches();
        $('#email_input').val($(this).html());
        $('#email_input').focus();
    });
    $('#email_input_autofill li').live('hover', function() {
        $('.selected').removeClass('selected');
        $(this).addClass('selected');
        selectedIndex = $('#email_input_autofill').children().index($(this)) + 1;
    });
    function showError(message) {
        var errorBox = $('#checkin_error');
        errorBox.html(message);
        if (!errorBox.is(':visible')) {
            errorBox.slideDown();
        }
    }
    function hideError() {
        $('#checkin_error').hide();
    }
    $('#checkin_form').submit(function(e) {
        var email = getEmail();
        var data = {'email': email };
        data.name = getName();
        $.post(CHECKIN_URL, data, function(res) {
            if (res.valid) {
                $('#checkin_status').removeClass();
                $('#checkin_status').addClass('success');

                var newLi = $('#checkins_li_template').clone();
                newLi.children('.name').eq(0).html(res.name);
                newLi.children('.email').eq(0).html(res.email);
                newLi.attr('id','');
                $('#checkins').prepend(newLi);

                newLi.effect('highlight', {}, 3000);
                $('#name_input').val('');
                $('#email_input').val('').focus();
                $("#event_checkin_count_num").text(1 + parseInt($("#event_checkin_count_num").text()));
            } else {
                $('#checkin_status').removeClass();
                $('#checkin_status').addClass('error');
                showError(res.error);
            }
        });
        e.preventDefault();
    });

    var hasClickedClose = false;
    $('#close_box').click(function() {
        if (!hasClickedClose) {
            $(this).animate({'opacity': 0});
            $('#close_dialogue').animate({'opacity': 0});
            hasClickedClose = true;
        }
    });
    $('#close_box').hover(
        function() {
            if (hasClickedClose) {
                $(this).stop().animate({'opacity': 1});
            }
        },
        function() {
            if (hasClickedClose) {
                $(this).stop().animate({'opacity': 0});
            }
        }
    );
    $('#close_button').click(function(e) {
        $('#event_checkin_main').addClass('hid').animate({
            opacity: 0
        });
        $('body').removeClass('overflowHidden');
        $('#event_checkin_link').children('.filler').eq(0).animate({
            height: '0%'
        });
        $('#event_checkin_link').removeClass('filled');
    });
    
    $('#event_tabs h2').each(function(i) {
        $(this).click(function() {
            $('.responses').addClass('hid');
            $('.responses').eq(i).removeClass('hid');
            $('.current').removeClass('current');
            $(this).addClass('current');
        });
    });

    $('#event_resume_drop').live('click', function(e) {
        var disabled = $(this).attr('disabled');
        if (!(typeof disabled !== 'undefined' && disabled !== false)) {
            $.post(EVENT_DROP_URL, function() {
                dropResume();
            });
        }
        e.preventDefault()
    });

    $('#event_resume_undrop').live('click', function(e) {
        var disabled = $(this).attr('disabled');
        if (!(typeof disabled !== 'undefined' && disabled !== false)) {
            var that = this;
            $.post(EVENT_UNDROP_URL, function() {
                undropResume();
            });
        }
        e.preventDefault()
    });
    
    $("#rsvp-yes-button[disabled=disabled]").tipsy({'gravity':'e', opacity: 0.9, fallback:RSVP_YES_TOOLTIP, html:true});
    $("#event_resume_drop[disabled=disabled]").tipsy({'gravity':'w', opacity: 0.9, fallback:DROP_RESUME_TOOLTIP, html:true});

    $('#name_input, #email_input').placeholder();
});
