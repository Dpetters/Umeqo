/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {

    var search_form_validator = $("#search_form").validate({
        errorPlacement: place_errors,
        rules: {
            query: {
                required: true,
            }
        },
        messages: {
            query: "Please supply a query"
        }
    });

    $('.delete-event-link').live('click',function(e) {
        $.post($(this).attr('href'),function(data) {
            console.log(data);
        });
        e.preventDefault();
    });
    
});
