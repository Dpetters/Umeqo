$(document).ready(function(){
    $("#recruiter_toggle_link").click(function() {
        $("#tutorial_notice a").show();
        $("#tutorial_notice span").hide();
        $("#recruiter_toggle_link").hide();
        $("#recruiter_toggle_span").show();
        $("#anonymous_student_tutorials").hide();
        $("#anonymous_campus_org_tutorials").hide();
        $("#anonymous_recruiter_tutorials").show();
    });
    $("#student_toggle_link").click(function() {
        $("#tutorial_notice a").show();
        $("#tutorial_notice span").hide();
        $("#student_toggle_link").hide();
        $("#student_toggle_span").show();
        $("#anonymous_recruiter_tutorials").hide();
        $("#anonymous_campus_org_tutorials").hide();
        $("#anonymous_student_tutorials").show();
    });
    $("#campus_org_toggle_link").click(function() {
        $("#tutorial_notice a").show();
        $("#tutorial_notice span").hide();
        $("#campus_org_toggle_link").hide();
        $("#campus_org_toggle_span").show();
        $("#anonymous_student_tutorials").hide();
        $("#anonymous_recruiter_tutorials").hide();
        $("#anonymous_campus_org_tutorials").show();
    }); 
});
