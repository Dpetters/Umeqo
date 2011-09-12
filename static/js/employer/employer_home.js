$(document).ready( function () {
    $(".must_be_subscribed_profile").tipsy({'gravity':'w', opacity: 0.9, live:true, fallback:"Please note that your profile is not visible to students (and therefore they cannot subscribe to you), unless you have an annual subscription.", html:true});

    $("#search_form_submit_button").live('click', function(e){
        if (!$("#query_field").val()){
            setTimeout(function() {
                $("#query_field").focus();
            }, 3000);
            e.preventDefault();
        }
    });
});
