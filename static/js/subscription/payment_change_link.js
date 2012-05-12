$("#payment_change_link a").live("click", function(){
    $("#payment_change_link").hide();
    $("#active_card").hide();
    $("#card_fields").removeClass("hid");
});