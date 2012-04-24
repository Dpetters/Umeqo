$(document).ready(function(){
    if (get_parameter_by_name("action")=="open_subscription_request_dialog"){
        $(".open_subscription_request_dialog_link").click();
    }
    $(".first .learn_more, .on .learn_more").popover({
        placement:"right",
    });
    $(".last .learn_more").popover({
        placement:"left",
    });
});