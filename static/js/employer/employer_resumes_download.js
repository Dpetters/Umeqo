function resumes_download_click_handler(e){
    $.ajax({
        type: 'GET',
        url: RESUMES_DOWNLOAD_URL,
        dataType: "json",
        beforeSend: function (jqXHR, settings) {
            
        },
        success: function (data) {
            console.log(data);
        },
        error: errors_in_message_area_handler
    });
    e.preventDefault(); 
}

$(".resumes_download").live("click", resumes_download_click_handler);