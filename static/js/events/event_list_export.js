function open_event_list_export_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        dialogClass: "event_list_export_dialog",
        modal:true,
        width:420,
        resizable: false,
        close: function(event, ui) {
            event_list_export_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function handle_export_event_list_link_click(e) {
    event_list_export_dialog = open_event_list_export_dialog();
    event_list_export_dialog.html(DIALOG_AJAX_LOADER);
    
    var event_id = $(this).attr("data-event-id");
    var event_list = $(this).attr("data-event-list");
    var event_name = $(this).attr("data-event-name");
    if (event_list == "attendees"){
        event_list_export_dialog.dialog("option", "title", "Export \"" + $(this).attr("data-event-name") + "\" Attendees");
    } else if (event_list == "rsvps"){
        event_list_export_dialog.dialog("option", "title", "Export \"" + $(this).attr("data-event-name") + "\" RSVPs");
    } else if (event_list == "all"){
        event_list_export_dialog.dialog("option", "title", "Export \"" + $(this).attr("data-event-name") + "\" All Responses");
    }
    
    var event_list_export_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        data: {"event_id":event_id, "event_list":event_list},
        dataType: "html",
        url: EVENT_LIST_EXPORT_URL,
        complete: function(jqXHR, textStatus) {
            clearTimeout(event_list_export_dialog_timeout);
            event_list_export_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                event_list_export_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                event_list_export_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            event_list_export_dialog.html(data);

            $("label[for=id_emails]").addClass('required').append("<span class='error'>*</span>");
            $("#id_emails").autoResize({
                animateDuration : 0,
                extraSpace : 18
            }).live('blur', function(){
                $(this).height(this.offsetHeight-28); 
            });
            
            $("#id_delivery_type").multiselect({
                height:53,
                header:false,
                minWidth:180,
                selectedList: 1,
                multiple: false,
                click: function(event, ui) {
                    console.log($("#id_delivery_type").multiselect("getChecked")[0].value);
                    console.log(EMAIL_DELIVERY_TYPE);
                    if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                        $('.email_delivery_type_only_field').show()
                        $('#id_emails').rules("add", {
                            multiemail: true,
                            required: true
                        });
                        $("#event_list_export_form input[type=submit]").val("Email");
                    } else {
                        $('.email_delivery_type_only_field').hide();
                        $('#id_emails').rules("remove", "email required");
                        $("#event_list_export_form input[type=submit]").val("Download");
                    }
                }
            });

            $("#id_export_format").multiselect({
                height:54,
                header:false,
                minWidth:180,
                selectedList: 1,
                multiple: false
            });
                        
            var event_list_export_form_validator = $("#event_list_export_form").validate({
                submitHandler: function(form) {
                    $("#event_list_export_form .error_section").html("");
                    if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                        $(form).ajaxSubmit({
                            dataType: 'html',
                            beforeSubmit: function (arr, $form, options) {
                                $("#event_list_export_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#event_list_export_form");
                            },
                            complete: function(jqXHR, textStatus) {
                                $("#event_list_export_form input[type=submit]").removeAttr("disabled");
                                event_list_export_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#event_list_export_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                if(jqXHR.status==0){
                                     event_list_export_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                }else{
                                     event_list_export_dialog.html(ERROR_MESSAGE_DIALOG);
                                }
                            },
                            success: function(data) {
                                event_list_export_dialog.html(data);
                            }
                        });
                    } else {
                        show_form_submit_loader("#event_list_export_form");
                        $("#event_list_export_form input[type=submit]").attr("disabled", "disabled");
                        var download_url = EVENT_LIST_DOWNLOAD_URL + "?event_id=" + event_id + "&event_list=" + event_list + "&export_format=" + escape($("#id_export_format").val());
                        window.location.href = download_url;
                        setTimeout(function(){
                            $.ajax({
                                dataType: "html",
                                url: EVENT_LIST_EXPORT_COMPLETED_URL + "?list=" + event_list,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        event_list_export_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                        event_list_export_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                },
                                success: function (data) {
                                    $(".event_list_export_dialog .dialog_content_wrapper").css("padding", "10px 15px 0px");
                                    event_list_export_dialog.html(data);
                                    event_list_export_dialog.dialog('option', 'title', 'Export Completed');
                                }
                            });
                        }, 1000);
                     }
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    export_format: {
                        required: true
                    },
                    delivery_type: {
                        required: true
                    }
                }
            });
        }
    });
    e.preventDefault();
}

$(document).ready(function(){
    $(".export_event_list_link").live('click', handle_export_event_list_link_click);
});