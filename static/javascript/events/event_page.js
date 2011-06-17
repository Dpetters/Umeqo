$(document).ready(function(){
    $('#attending-button').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            if (typeof data['valid']!='undefined' && data['valid']==true) {
                that.parent().fadeOut(200,function() {
                    var newText = $('<span id="attending-span">Attending</span>');
                    var newLink = $('<a href="" id="not-attending-button">RSVP: Not attending</a>');
                    newLink.attr('href',EVENT_UNRSVP_URL);
                    that.replaceWith(newText);
                    newText.after(newLink);
                });
                that.parent().fadeIn();
            }
        },"json");
        e.preventDefault();
    });
    $('#not-attending-button').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            if (typeof data['valid']!='undefined' && data['valid']==true) {
                that.parent().fadeOut(200,function() {
                    var newText = $('<a href="" id="attending-button" class="button">RSVP: Attending</a>');
                    newText.attr('href',EVENT_RSVP_URL);
                    that.replaceWith(newText);
                    $('#attending-span').remove();
                });
                that.parent().fadeIn();
            }
        },"json");
        e.preventDefault();
    });
    $('.event_rsvp').each(function() {
        $(this).click(function() {
            var id = $(this).attr('id');
            $('#f-'+id).submit();
        });
    });
    $('#event_signin_link').click(function(e) {
        $(this).children('.filler').eq(0).animate({
            height: '100%'
        }, function() {
            $.get(EVENT_RSVP_URL, function(data) {
                rsvps = data['rsvps'];
                rsvps_lookup = data['rsvps_lookup'];
                $('#event_signin_main').removeClass('hid').animate({
                    opacity: 1.0
                });
                $('body').css('overflow', 'hidden');
            });
        });
        $('#email_input').keyup(function(e) {
            var email = $(this).val();
            if (e.which == 40) {
                moveHighlight(1);
            } else if (e.which == 38) {
                moveHighlight(-1);
            } else if (email.length > 1){
                userText = email;
                var matches = findRSVPMatches(email);
            } else {
                clearMatches();
            }
        });
        $(this).addClass('filled');
        e.preventDefault();
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
    var rsvps, rsvps_lookup;
    var selectedIndex = 0;
    var userText = "";
    function clearMatches() {
        $('#email_input_autofill').empty();
        selectedIndex = 0;
    }
    function findRSVPMatches(ref_email) {
        clearMatches();
        for (var i=0; i<rsvps.length; i++) {
            rsvp = rsvps[i];
            if (rsvp.email.indexOf(ref_email) === 0 && $('#email_input_autofill li').length < 5) {
                $('#email_input_autofill').append($('<li>'+rsvp.email+'</li>'));
            }
        }
    }
    function moveHighlight(direction) {
        if (direction == -1 && selectedIndex>0) {
            selectedIndex--;
        } else if (direction == 1 && selectedIndex<$('#email_input_autofill li').length) {
            selectedIndex++;
        }
        $('.selected').removeClass('selected');
        var selectedLi = $('#email_input_autofill li').eq(selectedIndex-1)
        if (selectedIndex>0) {
            selectedLi.addClass('selected');
            $('#email_input').val(selectedLi.html());
        } else {
            $('#email_input').val(userText);
        }
    }
    function submitEmail(email) {
        var student_id = rsvps_lookup[email];
        console.log(student_id);
    }
    //$('#event_signin_link').click();
});
