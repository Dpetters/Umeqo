/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

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
});
