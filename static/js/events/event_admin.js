$(".expand_responses").live('click', function(){
   if ($(".rest_of_responses").is(":visible")){
       $(".rest_of_responses").slideUp();
       $(this).hide();
       $(".expand_responses.show").show();
   } else {
       $(".rest_of_responses").slideDown();
       $(this).hide();
       $(".expand_responses.hide").show()
   }
});