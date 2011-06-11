  $(document).ready(function() {
        var sliderWidth=$('#firm_thumb_scroller').width();
        var itemWidth=$('#firm_thumb_scroller .firm_thumb_content').width();
        $('#firm_thumb_scroller .firm_thumb_content').each(function (i) {
                        totalContent=i*itemWidth;    
                        $('#firm_thumb_scroller #firm_thumb_container').css("width",totalContent+itemWidth);
        });
        $('#firm_thumb_scroller').mousemove(function(e){
          var mouseCoords=(e.pageX - $(this).offset().left);
          var mousePercentY=mouseCoords/sliderWidth;
          var destY=-(((totalContent-(sliderWidth-itemWidth))-sliderWidth)*(mousePercentY));
          var thePosA=mouseCoords-destY;
          var thePosB=destY-mouseCoords;
          var animSpeed=600; //ease amount
          var easeType='easeOutCirc';
              if(mouseCoords==destY){
                      $('#firm_thumb_scroller #firm_thumb_container').stop();
              }
          else if(mouseCoords>destY){
                  //$('#thumbScroller .container').css('left',-thePosA); //without easing
                  $('#firm_thumb_scroller #firm_thumb_container').stop().animate({left: -thePosA}, animSpeed,easeType); //with easing
          }
          else if(mouseCoords<destY){
                  //$('#thumbScroller .container').css('left',thePosB); //without easing
                  $('#firm_thumb_scroller #firm_thumb_container').stop().animate({left: thePosB}, animSpeed,easeType); //with easing
          }
        });
        $('#firm_thumb_scroller .firm_thumb').each(function () {
          $(this).stop().css('border', '1px solid #808080');
        });
        var fadeSpeed=300;
        $('#firm_thumb_scroller .firm_thumb').hover(
                function(){ //mouse over
                        $(this).stop().css('border', '1px solid #606060');
                        var theText=$(this).attr('title');
                        console.log($(this));
                        $('#firm_name').html(theText);
                },
                function(){ //mouse out
                        $(this).stop().css('border', '1px solid #808080');
                        $('#firm_name').html('Firms using Umeqo');
                }
        );
    });