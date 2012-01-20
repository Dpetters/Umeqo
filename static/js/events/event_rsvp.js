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
        $dropdown.removeClass("dropdown").addClass("gray_button");
        that = $dropdown;
        rsvp_mouseout = true;
    }else{
           that = this;
       }
    $.ajax({
        type:'POST',
        url: RSVP_URL,
        data:{ attending: attending },
        beforeSend:function(){
            $(that).html("processing...");
            $("#rsvp_no, #rsvp_yes").live('mouseout', function(){
                rsvp_mouseout = true;
            });
            $("#rsvp_no, #rsvp_yes").live('mouseover', function(){
                rsvp_mouseout = false;
            });
        },
        success: function(data) {
            if(attending){
                $(that).removeClass("not_attending").addClass("attending").attr("id", "rsvp_no");
                if(rsvp_mouseout){
                    $(that).html("Attending");
                }else{
                    $(that).html("RSVP Not Attending");    
                }
            }else{
                $(that).removeClass("attending").addClass("not_attending").attr("id", "rsvp_yes");
                if(rsvp_mouseout){
                    $(that).html("Not Attending");
                }else{
                    $(that).html("RSVP Attending");    
                }
            }
        },
        error: errors_in_message_area_handler
    });
    
    if (attending) {
        resume_drop_mouseout = true;
        $("#drop_resume").click();
    }
}

function show_rsvp_message(){
    $.ajax({
        data:{'event_id':EVENT_ID},
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
    $(this).html("RSVP Not Attending");
});
$(".attending").live('mouseleave', function(){
    $(this).html("Attending");
});

$(".not_attending").live('mouseenter', function(){
    $(this).html("RSVP Attending");
});
$(".not_attending").live('mouseleave', function(){
    $(this).html("Not Attending");
});

$('#rsvp_yes').live('click', function(e) {
    show_rsvp_message();
    
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        rsvp.apply(this, [true]);
    }
});
$('#rsvp_no').live('click', function(e) {
    var disabled = $(this).attr('disabled');
    if (!(typeof disabled !== 'undefined' && disabled !== false)) {
        rsvp.apply(this, [false]);
    }
});
    
$(document).ready(function(){
    if (get_parameter_by_name("rsvp")=="true"){
        rsvp_mouseout = true;
        $("#rsvp_yes, #rsvp_button").click();
    }
    if (get_parameter_by_name("rsvp")=="false"){
        rsvp_mouseout = true;
        $("#rsvp_no").click();
    }
    $("#rsvp_requires_login").tipsy({'gravity':'e', opacity: 0.9, fallback:"RSVP requires login.", html:true});
    $("#rsvp_yes[disabled=disabled], #rsvp_choices[disabled=disabled]").tipsy({'gravity':'e', opacity: 0.9, fallback:RSVP_YES_TOOLTIP, html:true});
});