$(document).ready(function() {
    $("#change_payment a").live("click", function(){
        $(this).hide();
        $("#active_card").hide();
        $("#card_form").removeClass("hid");
    });
});