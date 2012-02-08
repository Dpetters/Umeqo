var resume_drop_mouseout = false;
function resume_drop(drop){
    var that = this;
    $.ajax({
        type:"POST",
        url:RESUME_DROP_URL,
        data: {'drop':drop},
        beforeSend: function(){
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
                $(that).addClass("undrop_resume resume_dropped");
                if(resume_drop_mouseout){
                    $(that).html("Resume Dropped");
                }else{
                    $(that).html("Undrop Resume");
                }
            }else{
                $(that).removeClass("resume_dropped").html("Drop Resume");
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