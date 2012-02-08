$(".expand_responses").live('click', function(){
    if ($(this).prevAll(".rest_of_responses").is(":visible")){
        $(this).prevAll(".rest_of_responses").slideUp();
        $(this).hide();
        $(this).prev().show();
    } else {
        $(this).prevAll(".rest_of_responses").slideDown();
        $(this).hide();
        $(this).next().show()
    }
});