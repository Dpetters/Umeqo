/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {
	$("#search_form_submit_button").live('click', function(e){
		if (!$("#query_field").val()){
			$("#query_field").focus();
			e.preventDefault();
		}
	});

    $('.delete-event-link').live('click',function(e) {
        var that = $(this);
        $.post($(this).attr('href'),function(data) {
            console.log(that.parentsUntil('div'));
            var li = that.parentsUntil('ul')
            li.slideUp(function(){
                li.remove();
                if ($('.event_list:eq(0) li').length==0) {
                    $('#no_events_block').slideDown();
                }
            });
        });
        e.preventDefault();
    });
    
});
