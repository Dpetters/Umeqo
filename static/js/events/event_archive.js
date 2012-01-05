$(document).ready( function () {
    $('.archive_event_link').live('click', function (e) {
        var that = this;
        var li = $(that).parents("li");
        var ul = li.parent();
        $.ajax({
            type:"POST",
            dataType: "json",
            url: $(that).attr("href"),
            success: function (data){
	            if (li.length != 0){
	                li.slideUp(function(){
	                    li.remove();
	                    if ($('.event_list li').length==0){
	                        $('#event_filtering_no_results').slideDown();
	                    }
	                });
	                if(data.type=="event")
	                   $("#message_area").html("<p>" + EVENT_ARCHIVED + "</p>");
	            	else
	                   $("#message_area").html("<p>" + DEADLINE_ARCHIVED + "</p>");                            	
	            }else{
	                window.location.href="/?msg=" + data.type + "-cancelled";
	            }
  			}
  		});
        e.preventDefault();
	});
});