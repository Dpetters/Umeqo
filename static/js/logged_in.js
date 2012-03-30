$(document).ready( function() {
    
    $(".premium_required").tipsy({'gravity':'w', opacity: 0.9, live:true, fallback:PREMIUM_REQUIRED, html:true}); 
    $(".premium_required").tipsy({'gravity':'e', opacity: 0.9, live:true, fallback:PREMIUM_REQUIRED, html:true}); 
    $(".premium_required").tipsy({'gravity':'n', opacity: 0.9, live:true, fallback:PREMIUM_REQUIRED, html:true}); 
    $(".premium_required").tipsy({'gravity':'s', opacity: 0.9, live:true, fallback:PREMIUM_REQUIRED, html:true}); 
               
    $('#account').click(function() {
       // We subtract two for the border
       $('#account_dropdown').width(document.getElementById("account").offsetWidth-2).toggle(); 
       if ($(this).hasClass('pressed')) $(this).removeClass('pressed');
       else $(this).addClass('pressed');
    });
    $('body').click(function(event) {
        if (!$(event.target).closest('#account').length && !$(event.target).closest('#account_dropdown').length) {
            $('#account_dropdown').hide();
            $('#account').removeClass('pressed');
        };
    }); 

    // NOTIFICATIONS.
    $('#notifications_count').click(function() {
        if (!$('#notifications_pane').is(':visible')) {
            $.get(NOTIFICATIONS_URL, function(data) {
                $('#notifications_pane').html(data);
            });
            $('#notifications_number').addClass('invisible');
            $('#notifications_count').addClass('pressed');
        } else {
            $('#notifications_count').removeClass('pressed');
        }
        $('#notifications_pane').toggle();
    });
    $(document).keydown(function(e) {
        if (e.which == 27) {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('pressed');
        }
    });
    $(document).click(function(e) {
        if ($(e.target).parents('#notifications_pane').length == 0 &&
            e.target.id != 'notifications_count') {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('pressed');
        }
    });
});