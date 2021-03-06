var rsvp_mouseout = false;

function open_rsvp_info_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"RSVP Message",
        dialogClass: "rsvp_info_dialog",
        modal:true,
        width:550,
        resizable: false,
        close: function() {
            rsvp_info_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function rsvp(attending) {
    var $dropdown = $(this).parents(".dropdown"),
        that = null;
        
    if($dropdown.length!=0){
        $dropdown.removeClass("dropdown");
        var that = $("<a href='#'>" + $(this).text() + "</a>");
        $dropdown.replaceWith(that);
        rsvp_mouseout = true;
    }else{
       that = $(this);
    }
   
    var parent = get_parent(that);
    // If the tagname is LI then this is an event snippet and we don't want the rsvp
    // links to be buttons
    if(parent[0].tagName != "LI"){
        that.addClass("button");
    }
    var is_deadline = $(parent).data("is-deadline")=="True";
    var rsvp_url = $(parent).data("rsvp-url");
    
    $.ajax({
        type:'POST',
        url: rsvp_url,
        data:{ attending: attending },
        beforeSend:function(){
            $("#message_area").html("");
            $(that).html("processing...");
            $(".rsvp_no, .rsvp_yes").live('mouseout', function(){
                rsvp_mouseout = true;
            });
            $(".rsvp_no, .rsvp_yes").live('mouseover', function(){
                rsvp_mouseout = false;
            });
        },
        success: function(data) {
            if(attending){
                $(that).removeClass("not_attending rsvp_yes").addClass("attending rsvp_no");
                if(rsvp_mouseout){
                    if (is_deadline)
                        $(that).html("Participating");
                    else
                        $(that).html("Attending");
                }else{
                    if(is_deadline)
                        $(that).html("RSVP Not Participating");
                    else
                        $(that).html("RSVP Not Attending");
                }
            }else{
                $(that).removeClass("attending rsvp_no").addClass("not_attending rsvp_yes");
                if(rsvp_mouseout){
                    if(is_deadline)
                        $(that).html("Not Participating");
                    else
                        $(that).html("Not Attending");
                }else{
                    if(is_deadline)
                        $(that).html("RSVP Participating");
                    else
                        $(that).html("RSVP Attending");
                }
            }
        },
        error: errors_in_message_area_handler
    });
    
    if (attending) {
        resume_drop_mouseout = true;
        $(parent).find(".drop_resume").click();
    }
}

function show_rsvp_message(event_id){
    $.ajax({
        data:{'event_id':event_id},
        url:RSVP_MESSAGE_URL,
        success: function(data) {
            if(data){
                rsvp_info_dialog = open_rsvp_info_dialog();
                rsvp_info_dialog.html(data);
            }
        },
        error: errors_in_message_area_handler
    });
}

$(".attending").live('mouseenter', function(){
    var parent = get_parent(this);
    if($(parent).data("is-deadline")=="True"){
        $(this).html("RSVP Not Participating");
    }else{
        $(this).html("RSVP Not Attending");
    }
});
$(".attending").live('mouseleave', function(e){
    var parent = get_parent(this);
    if($(parent).data("is-deadline")=="True")
        $(this).html("Participating");
    else
        $(this).html("Attending");
});

$(".not_attending").live('mouseenter', function(e){
    var parent = get_parent(this);
    if($(parent).data("is-deadline")=="True")
        $(this).html("RSVP Participating");
    else
        $(this).html("RSVP Attending");
});
$(".not_attending").live('mouseleave', function(e){
    var parent = get_parent(this);
    if($(parent).data("is-deadline")=="True")
        $(this).html("Not Participating");
    else
        $(this).html("Not Attending");
});

$('.rsvp_yes').live('click', function(e) {
    var parent = get_parent(this);
    show_rsvp_message($(parent).data("event-id"));
    
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        rsvp.apply(this, [true]);
    }
    e.preventDefault();
});
$('.rsvp_no').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        rsvp.apply(this, [false]);
    }
    e.preventDefault();
});
