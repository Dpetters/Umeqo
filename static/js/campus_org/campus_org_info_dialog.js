$(document).ready(function() {
    function open_campus_org_info_dialog(campus_org_name) {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:campus_org_name,
            dialogClass: "campus_org_info_dialog",
            modal:true,
            width:550,
            resizable: false,
            close: function() {
                campus_org_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    function campus_org_profile_link_click_handler(e) {
        campus_org_info_dialog = open_campus_org_info_dialog($(this).attr('data-campus-org-name'));
        campus_org_info_dialog.html(DIALOG_AJAX_LOADER);
        campus_org_id = $(this).attr('data-campus-org-id');
        var campus_org_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            type: 'GET',
            url: CAMPUS_ORG_INFO_URL,
            dataType: "html",
            data: { 'campus_org_id': campus_org_id },
            complete: function(jqXHR, textStatus) {
                clearTimeout(campus_org_info_dialog_timeout);
                campus_org_info_dialog.dialog('option', 'position', 'center');
            },
            success: function (data) {
                campus_org_info_dialog.html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    campus_org_info_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    campus_org_info_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            }
        });
        e.preventDefault();
    };
        
    $(".campus_org_profile_link").live('click', campus_org_profile_link_click_handler);
});