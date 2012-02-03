console.log("loaded");
$(".expand_responses").live('click', function(){
   console.log("hey");
   if ($(".rest_of_responses").is(":visible")){
       $(".rest_of_responses").hide();
   } else {
       $(".rest_of_responses").show();
   }
});
