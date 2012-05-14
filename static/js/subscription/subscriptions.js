$(document).ready(function(){
    if (get_parameter_by_name("action")=="request_basic_account"){
        $(".request_account_link[subscription-type=basic]").click();
    } else if (get_parameter_by_name("action")=="request_premium_account"){
        $(".request_premium_account_link[subscription-type=premium]").click();
    } else if (get_parameter_by_name("action")=="request_enterprise_account"){
        $(".request_enterprise_account_link[subscription-type=enterprise]").click();
    }
    
    $(".first .learn_more, .on .learn_more").popover({
        placement:"right",
    });
    $(".last .learn_more").popover({
        placement:"left",
    });
});