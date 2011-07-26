$(document).ready(function() {
    var cloudmade = new CM.Tiles.CloudMade.Web({key: '5107685de1ba4ebcbcfccc6335bd1eec'});
    var map = new CM.Map('cm-example', cloudmade);
    map.setCenter(new CM.LatLng(42.35995437, -71.08686692), 18);
 
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
    }
    $('#rsvp-yes-button').live('click', function(e) {
        if ($(this).hasClass('selected')) {
            return false;
        }
        rsvp.apply(this, [true]);
        if ($(this).hasClass('left-group')) {
            $('#rsvp_div .selected').removeClass('selected');
            $(this).addClass('selected');
        }
        e.preventDefault();
    });
    $('#rsvp-no-button').live('click', function(e) {
        if ($(this).hasClass('selected')) {
            return false;
        }
        rsvp.apply(this, [false]);
        if ($(this).hasClass('right-group')) {
            $('#rsvp_div .selected').removeClass('selected');
            $(this).addClass('selected');
        }
        e.preventDefault();
    });
    $('#remove-rsvp-button').live('click', function(e) {
        $.post($(this).attr('href'), function(data) {
            if (typeof data.valid != 'undefined' && data.valid == true) {
                $('.response').removeClass('hid');
                $('.no-response').addClass('hid');
                $('#rsvp_div .selected').removeClass('selected');
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
        $(this).children('.filler').eq(0).animate({
            height: '100%'
        }, function() {
            $.get(EVENT_RSVP_URL, function(data) {
                rsvps = data;
                $.get(CHECKIN_URL, function(data) {
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
                });
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
                $(this).parent('form').submit();
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
});
