$(document).ready( function () {

   function handle_firm_size_option_change() {
      switch($(this).val()){
          case 'S':
               url = SMALL_EMPLOYER_URL;
               break;
          case 'M':
               url = MEDIUM_EMPLOYER_URL;
               break;
          case 'L':
               url = LARGE_EMPLOYER_URL;
               break;
          case 'P':
               url = NONPROFIT_URL;
               break;
          default:
               break;
      }

      if (typeof(url)!="undefined"){
          window.location = url;
      }
   };
   
   $("#firm_size").change(handle_firm_size_option_change);
   $("#firm_size").val("");
});
