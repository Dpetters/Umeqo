$(document).ready(function(){
    if (get_parameter_by_name("rsvp")=="true"){
        rsvp_mouseout = true;
        $(".rsvp_yes, #rsvp_button").click();
    }
    if (get_parameter_by_name("rsvp")=="false"){
        rsvp_mouseout = true;
        $(".rsvp_no").click();
    }
    $(".rsvp_yes[disabled=disabled], .rsvp_choices[disabled=disabled]").tipsy({'gravity':'e', opacity: 0.9, fallback:RSVP_YES_TOOLTIP, html:true});
});