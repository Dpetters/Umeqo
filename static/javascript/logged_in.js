/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
    $.idleTimeout('#idletimeout_block', '#idletimeout_block a', {
        idleAfter: 1800,
        onTimeout: function() {
            $(this).slideUp();
            window.location = "/logout/?next=/?action=timed-out";
        },
        onIdle: function() {
            $(this).slideDown(); // show the warning bar
        },
        onCountdown: function(counter) {
            $(this).find("span").html(counter); // update the counter
        },
        onResume: function() {
            $(this).slideUp(); // hide the warning bar
        }
    });
    
    /* Objects */
    query_field_default_text = "Search by keywords, skills, etc";
    
    $('#account_dropdown').hide();
    $('#account').click(function() {
       $('#account_dropdown').toggle(); 
       if ($(this).hasClass('pressed')) $(this).removeClass('pressed');
       else $(this).addClass('pressed');
    });
    $('body').click(function(event) {
        if (!$(event.target).closest('#account').length) {
            $('#account_dropdown').hide();
            $('#account').removeClass('pressed');
        };
    });
    
});
