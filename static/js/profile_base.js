$(document).bind("widgetsLoaded", function(e){
    var current = 0;  // Current Page
    accordion = $("#stepForm").accordion({
        autoHeight:false,
        animated:false
    });
    accordion.accordion( "option", "active", parseInt(get_parameter_by_name("page"))); 
    
    // Set up multipart form navigation
    $(".navigation").click( function() {
        if (current < this.id) {
            if (v.form()) {
                accordion.accordion("activate", parseInt(this.id));
                current = parseInt(this.id);
            }
        } else {
            accordion.accordion("activate", parseInt(this.id));
            current = parseInt(this.id);
        }
    });
});