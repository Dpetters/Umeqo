$(document).ready( function () {
    $("#search_form_submit_button").live('click', function(e){
        if (!$("#query_field").val()){
            setTimeout(function() {
                $("#query_field").focus();
            }, 3000);
            e.preventDefault();
        }
    });
});
