$(document).ready(function(){
    // Back buttons do not need to run validation
    $("#pg2 .open0").click( function() {
        accordion.accordion("activate", 0);
        current = 0;
    });
    
    // Next buttons need to run validation
    $("#pg1 .open1").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 1);
            current = 1;
        }
    }); 
});
