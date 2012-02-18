var resume_drop_mouseout = false;
function resume_drop(drop){
    var that = this;
    var parent = get_parent(that);
    var resume_drop_url = $(parent).data("rsvp-url");

    $.ajax({
        type:"POST",
        url:resume_drop_url,
        data: {'drop':drop},
        beforeSend: function(){
            $("#message_area").html("");
            $(that).html("processing...");
            $(".drop_resume").live('mouseout', function(){
                resume_drop_mouseout = true;
            });
            $(".drop_resume").live('mouseover', function(){
                resume_drop_mouseout = false;
            });
        },
        success:function() {
            if (drop){
                $(that).addClass("undrop_resume resume_dropped").removeClass("drop_resume");
                if(resume_drop_mouseout){
                    $(that).html("Resume Dropped");
                }else{
                    $(that).html("Undrop Resume");
                }
            }else{
                $(that).removeClass("resume_dropped undrop_resume").addClass("drop_resume").html("Drop Resume");
            }
        },
        error: errors_in_message_area_handler
    });    
}
$('.drop_resume').live('click', function(e) {
    var that = this;
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        resume_drop.apply(this, [true]);
    }
});

$('.undrop_resume').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        resume_drop.apply(this, [false]);
    }
});

$(".resume_dropped").live('mouseover', function(){
    $(this).html("Undrop Resume");
});
$(".resume_dropped").live('mouseout', function(){
    $(this).html("Resume Dropped");
});