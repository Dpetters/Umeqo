$(document).ready(function(){
    $(".question_link").live("click", function(){
        var question_id = $(this).attr("data-id");
        $.ajax({
            type:"POST",
            data:{
                'question_id':question_id
            },
            dataType: "json",
            url: FAQ_URL
        });
    })        
});
