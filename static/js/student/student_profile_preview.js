function handle_student_hide_details_link_click() {
    var id = $(this).attr('data-student-id');
    $('.student_detailed_info[data-student-id=' + id  + ']').slideUp('slow');
    $('.student_toggle_detailed_info_link[data-student-id=' + id  + ']').html(SHOW_DETAILS_LINK);
};

function handle_student_toggle_detailed_info_link_click() {
    var id = $(this).attr('data-student-id');
    if ($(this).children('span').attr('class') === "hide_details") {
        $('.student_detailed_info[data-student-id=' + id  + ']').slideUp('slow');
        $(this).html(SHOW_DETAILS_LINK);
    } else {
        $('.student_detailed_info[data-student-id=' + id  + ']').slideDown('slow');
        $(this).html(HIDE_DETAILS_LINK);
    }
};
    
$(".student_toggle_detailed_info_link").live('click', handle_student_toggle_detailed_info_link_click);
$(".student_hide_details_link").live('click', handle_student_hide_details_link_click);
$(".student_comment").live('blur', function(){ $(this).height(17); }); 