function handle_billing_cycle_change(e){
    $.ajax({
        url:
    })
    $("#price").html($('input[name=billing_cycle]:checked').parent().text().split("$")[1].split(" ")[0]);
}

$(document).ready(function() {
    $('input[name=billing_cycle]').live('change', handle_billing_cycle_change);
    handle_billing_cycle_change();
});