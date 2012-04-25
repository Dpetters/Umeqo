$(document).ready(function(){
    if (get_parameter_by_name("action")=="request_account"){
        $(".request_account_link").click();
    }
    $(".first .learn_more, .on .learn_more").popover({
        placement:"right",
    });
    $(".last .learn_more").popover({
        placement:"left",
    });
});