$(document).ready( function() {
    $('#account_dropdown').hide();
    $('#account').click(function() {
       $('#account_dropdown').toggle(); 
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
