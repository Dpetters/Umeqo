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
                        if (ul.children().length == 0)
                        {
                            ul.prev().remove();
                            ul.remove();
                        }
                        if ($('.event_list li').length==0){
                            $('#event_filtering_no_results').slideDown();
                            $("#no_events_block").slideDown()
                        }
                    });
                }else{
                    $("#event").addClass("archived");
                }
                if(data.type=="event")
                   $("#message_area").html("<p>" + EVENT_ARCHIVED + "</p>");
                else
                   $("#message_area").html("<p>" + DEADLINE_ARCHIVED + "</p>");  
              }
          });
        e.preventDefault();
    });
});