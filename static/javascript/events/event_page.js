$(document).ready(function () {
    $('#attending-button').live('click', function (e) {
        var that = $(this);
        $.post($(this).attr('href'), function (data) {
            if (typeof data.valid != 'undefined' && data.valid == true) {
                that.parent().fadeOut(200, function () {
                    var newText = $('<span id="attending-span">Attending</span>');
                    var newLink = $('<a href="" id="not-attending-button">RSVP: Not attending</a>');
                    newLink.attr('href', EVENT_UNRSVP_URL);
                    that.replaceWith(newText);
                    newText.after(newLink);
                });
                that.parent().fadeIn();
            }
        }, "json");
        e.preventDefault();
    });
    $('#not-attending-button').live('click', function (e) {
        var that = $(this);
        $.post($(this).attr('href'), function (data) {
            if (typeof data.valid != 'undefined' && data.valid == true) {
                that.parent().fadeOut(200, function () {
                    var newText = $('<a href="" id="attending-button" class="button">RSVP: Attending</a>');
                    newText.attr('href', EVENT_RSVP_URL);
                    that.replaceWith(newText);
                    $('#attending-span').remove();
                });
                that.parent().fadeIn();
            }
        }, "json");
        e.preventDefault();
    });
    $('.event_rsvp').each(function () {
        $(this).click(function () {
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
    $('#event_signin_link').click(function (e) {
        $(this).children('.filler').eq(0).animate({
            height: '100%'
        }, function () {
            $.get(EVENT_RSVP_URL, function (data) {
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
                    $('#event_signin_main').removeClass('hid').animate({
                        opacity: 1.0
                    });
                    $('body').addClass('overflowHidden');
                });
            });
        });
        $(this).addClass('filled');
        e.preventDefault();
    });
    $('#email_input').keydown(function (e) {
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
    $('#email_input').keyup(function (e) {
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
    $('#checkin_form input').each(function () {
        $(this).keyup(function (e) {
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
    $('#email_input_autofill li').live('click', function () {
        clearMatches();
        $('#email_input').val($(this).html());
        $('#email_input').focus();
    });
    $('#email_input_autofill li').live('hover', function () {
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
    $('#checkin_form').submit(function (e) {
        var email = getEmail();
        var data = {'email': email };
        data.name = getName();
        $.post(CHECKIN_URL, data, function (res) {
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
    $('#close_box').click(function () {
        if (!hasClickedClose) {
            $(this).animate({'opacity': 0});
            $('#close_dialogue').animate({'opacity': 0});
            hasClickedClose = true;
        }
    });
    $('#close_box').hover(
        function () {
            if (hasClickedClose) {
                $(this).stop().animate({'opacity': 1});
            }
        },
        function () {
            if (hasClickedClose) {
                $(this).stop().animate({'opacity': 0});
            }
        }
    );
    $('#close_button').click(function (e) {
        $('#event_signin_main').addClass('hid').animate({
            opacity: 0
        });
        $('body').removeClass('overflowHidden');
        $('#event_signin_link').children('.filler').eq(0).animate({
            height: '0%'
        });
        $('#event_signin_link').removeClass('filled');
    });
});
