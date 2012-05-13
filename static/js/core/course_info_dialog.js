$(document).ready(function() {
    function open_course_info_dialog(major_name) {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:major_name,
            dialogClass: "course_info_dialog",
            modal:true,
            width:550,
            resizable: false,
            close: function() {
                course_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

   function course_link_click_handler(e) {
        course_info_dialog = open_course_info_dialog($(this).text());
        course_info_dialog.html(DIALOG_AJAX_LOADER);
        var course_id = $(this).attr('data-major-id');
        var course_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            type: 'GET',
            url: COURSE_INFO_URL,
            dataType: "html",
            data: { 'course_id': course_id },
            complete: function(jqXHR, textStatus) {
                clearTimeout(course_info_dialog_timeout);
            },
            success: function (data) {
                course_info_dialog.html(data);
                course_info_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    course_info_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    course_info_dialog.html(ERROR_MESSAGE_DIALOG);
                }
                course_info_dialog.dialog('option', 'position', 'center');
            }
        });
        e.preventDefault();
    };
    
    $(".course_link").live('click', course_link_click_handler);
});