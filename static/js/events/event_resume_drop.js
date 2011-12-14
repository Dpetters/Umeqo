function resume_drop(drop){
	var that = this;
    $.ajax({
    	type:"POST",
    	url:RESUME_DROP_URL,
    	data: {'drop':drop},
    	beforeSend: function(){
    		$(that).html("processing...");
    	},
    	success:function() {
    		if (drop){
    			$(that).attr("id", "undrop_resume").addClass("resume_dropped").html("Resume Dropped");
    		}else{
    			$(that).attr("id", "drop_resume").removeClass("resume_dropped").html("Drop Resume");	    			
    		}
    	},
    	error: errors_in_message_area_handler
	});	
}
$('#drop_resume').live('click', function(e) {
	var that = this;
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
    	resume_drop.apply(this, [true]);
    }
});

$('#undrop_resume').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
    	resume_drop.apply(this, [false]);
    }
});
/*
$(".resume_dropped").live('mouseover', function(){
	$(this).html("Undrop Resume");
});
$(".resume_dropped").live('mouseout', function(){
	$(this).html("Resume Dropped");
});*/