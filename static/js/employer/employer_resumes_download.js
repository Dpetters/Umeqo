function resumes_all_click_handler(){
    console.log("clicked!");
    e.preventDefault(); 
}

$(".resumes_download").live("click", resumes_all_click_handler);