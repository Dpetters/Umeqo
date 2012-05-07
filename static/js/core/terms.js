$(document).ready( function () {
    $("#terms_tabs").tabs();
    
    if (get_parameter_by_name("tab")=="privacy-policy"){
        $("#terms_tabs").tabs("select", 1);
    } else if(get_parameter_by_name("tab")=="subscription-terms"){
        $("#terms_tabs").tabs("select", 2);
    } 
});