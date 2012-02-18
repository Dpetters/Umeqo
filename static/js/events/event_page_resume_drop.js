$(document).ready(function(){
    if (get_parameter_by_name("drop")=="true"){
        resume_drop_mouseout = true;
        $("#drop_resume, #drop_resume_button").click();
    }
    if (get_parameter_by_name("drop")=="false"){
        resume_drop_mouseout = true;
        $("#undrop_resume").click();
    }
    $(".drop_resume[disabled=disabled]").tipsy({'gravity':'e', opacity: 0.9, fallback:NOT_STUDENT_DROP_RESUME_TOOLTIP, html:true});
});