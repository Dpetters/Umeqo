function open_upload_recruiters_list_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        dialogClass: "upload_recruiters_list_dialog",
        title: "Upload Recruiters List",
        modal:true,
        width:520,
        resizable: false,
        close: function(event, ui) {
            upload_recruiters_list_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function handle_upload_recruiters_list_click(e) {
    upload_recruiters_list_dialog = open_upload_recruiters_list_dialog();
    upload_recruiters_list_dialog.html(DIALOG_AJAX_LOADER);
    
    var event_id = $(this).attr("data-event-id");
    
    var upload_recruiters_list_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        data: {"event_id":event_id},
        dataType: "html",
        url: UPLOAD_RECRUITERS_LIST_URL,
        complete: function(jqXHR, textStatus) {
            clearTimeout(upload_recruiters_list_dialog_timeout);
            upload_recruiters_list_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                upload_recruiters_list_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                upload_recruiters_list_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            upload_recruiters_list_dialog.html(data);
                        
            var upload_recruiters_list_form_validator = $("#upload_recruiters_list_form").validate({
                submitHandler: function(form) {
                    $("#upload_recruiters_list_form .error_section").html("");
                    $(form).ajaxSubmit({
                        dataType: 'json',
                        beforeSubmit: function (arr, $form, options) {
                            //disable the submit button
                            $("#upload_recruiters_list_form input[type=submit]").attr('disabled', 'disabled');
                            // show spinny
                            show_form_submit_loader("#upload_recruiters_list_form");
                            // if any errors were shown before, hide them
                            $("#upload_recruiters_list_form .error_selection").html("");
                        },
                        complete: function(jqXHR, textStatus) {
                            // enable submite button
                            $("#upload_recruiters_list_form input[type=submit]").removeAttr('disabled').focusout();
                            // hide spinny
                            hide_form_submit_loader("#upload_recruiters_list_form");
                        },
                        success: function(data) {
                            if(data.errors){
                                place_table_form_errors("#upload_recruiters_list_form", data.errors);
                            } else {
                                var success_message = "<div class='dialog_content_wrapper'><div class='message_section'><p>Recruiters uploaded successfully. Please <a href='#' class='refresh_page_link'>refresh the page</a> to update the event page.</p></div>";
                                success_message += CLOSE_DIALOG_LINK + "</div>";
                                upload_recruiters_list_dialog.html(success_message);
                            }
                            
                        },
                        error: errors_in_message_area_handler
                    });
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    csvfile: {
                        required: true
                    }
                },
                messages: {
                    csvfile: {
                        required: "This field is required."
                    }
                }
            });
        }
    });
    e.preventDefault();
}

$(document).ready(function(){
    $(".upload_recruiters_list").live('click', handle_upload_recruiters_list_click);
});
