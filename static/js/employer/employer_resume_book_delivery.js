function open_deliver_resume_book_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"Deliver Resume Book",
        dialogClass: "deliver_resume_book_dialog",
        modal:true,
        width:470,
        resizable: false,
        close: function(event, ui) {
            deliver_resume_book_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function post_delivery_cleanup(){
    if(typeof(update_resume_book_contents_summary)!="undefined"){
        update_resume_book_contents_summary();
        $(".resume_book_current_toggle_student").html(ADD_TO_RESUME_BOOK_IMG);
    }
}

function handle_deliver_resume_book_link_click() {
    deliver_resume_book_dialog = open_deliver_resume_book_dialog();
    deliver_resume_book_dialog.html(DIALOG_AJAX_LOADER);
    var that = $(this);
    var resume_book_created = false;
    var delivery_selection_text = 'Combine all resumes into one file';
    var delivery_type = 'book';
    var service_email = $('#email_delivery_type').prop('checked');

    var deliver_resume_book_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        data: {'resume_book_id':that.attr("data-resume-book-id")},
        dataType: "html",
        url: RESUME_BOOK_CURRENT_DELIVER_URL,
        complete: function(jqXHR, textStatus) {
            clearTimeout(deliver_resume_book_dialog_timeout);
            deliver_resume_book_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                deliver_resume_book_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                deliver_resume_book_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            deliver_resume_book_dialog.html(data);
            $("label[for=id_emails]").addClass('required').append("<span class='error'>*</span>");
            $("#id_emails").autoResize({
                animateDuration : 0,
                extraSpace : 18
            }).live('blur', function(){
                $(this).height(this.offsetHeight-28); 
            });
            
            $("#book_delivery_type").click(function(){
                $("#delivery_types img").removeClass("delivery_selection");
                $(this).addClass("delivery_selection");
                //TODO: Get rid of all this yucky hardcoded stuff
                delivery_type = 'book';
                delivery_selection_text = 'Combine all resumes into one file';
                $("#delivery_selection_text").text(delivery_selection_text);
                recreate_resume_file();
            });
            $("#book_delivery_type").hover(function(){
                $("#delivery_selection_text").text('Combine all resumes into one file');
            }, function() {
                $("#delivery_selection_text").text(delivery_selection_text);
            });

            $("#bundle_delivery_type").click(function(){
                $("#delivery_types img").removeClass("delivery_selection");
                $(this).addClass("delivery_selection");
                delivery_type = 'bundle';
                delivery_selection_text = 'Bundle of individual resumes';
                $("#delivery_selection_text").text(delivery_selection_text);
                recreate_resume_file();
            });
            $("#bundle_delivery_type").hover(function(){
                $("#delivery_selection_text").text('Bundle of individual resumes');
            }, function() {
                $("#delivery_selection_text").text(delivery_selection_text);
            });

            $("#email_delivery_type").click(function(){
                service_email = $(this).prop("checked");
                if (service_email) {
                    $(".email_delivery_type_only_field").show()
                    $("#id_emails").rules("add", {
                        multiemail: true,
                        required: true
                    });
                    $("#deliver_resume_book_form_submit_button").val("Email");
                    $("#bundle_delivery_type").hide();
                    $("#book_delivery_type").css("margin-left", "66px");
                    $("#delivery_types img").removeClass("delivery_selection");
                    $("#book_delivery_type").addClass("delivery_selection");
                    delivery_type = "book";
                    delivery_selection_text = "Combine all resumes into one file";
                    $("#delivery_selection_text").text(delivery_selection_text);
                    recreate_resume_file();
                }
                else {
                    $(".email_delivery_type_only_field").hide();
                    $("#id_emails").rules("remove", "email required");
                    $("#deliver_resume_book_form_submit_button").val("Download");
                    $("#book_delivery_type").css("margin-left", "25px");
                    $("#bundle_delivery_type").show();
                }
            });

            function recreate_resume_file() {
                resume_book_created = false;
                $("#deliver_resume_book_form_loader").css('display','inline');
                $.ajax({
                    type: "POST",
                    data:{'delivery_type':delivery_type,'resume_book_id':that.attr("data-resume-book-id")},
                    dataType: "json",
                    url: RESUME_BOOK_CURRENT_CREATE_URL,
                    error: function(jqXHR, textStatus, errorThrown) {
                        if(jqXHR.status==0){
                             deliver_resume_book_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                        }else{
                             deliver_resume_book_dialog.html(ERROR_MESSAGE_DIALOG);
                        }
                    },
                    success: function (data) {
                        resume_book_created = true;
                        $("#deliver_resume_book_form_loader").css('display','none');         
                    }
                });
            }
            var deliver_resume_book_form_validator = $("#deliver_resume_book_form").validate({
                submitHandler: function(form) {
                    if(resume_book_created) {
                        var custom_resume_book_name = $("#id_name").val();
                        $("#deliver_resume_book_form .error_section").html("");
                        if(service_email) {
                            $(form).ajaxSubmit({
                                data : { 'name' : custom_resume_book_name, 'resume_book_id':that.attr("data-resume-book-id")},
                                dataType: 'html',
                                beforeSubmit: function (arr, $form, options) {
                                    $("#deliver_resume_book_form input[type=submit]").attr("disabled", "disabled");
                                    show_form_submit_loader("#deliver_resume_book_form");
                                },
                                complete: function(jqXHR, textStatus) {
                                    $("#deliver_resume_book_form input[type=submit]").removeAttr("disabled");
                                    deliver_resume_book_dialog.dialog('option', 'position', 'center');
                                    hide_form_submit_loader("#deliver_resume_book_form");
                                },
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                         deliver_resume_book_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                         deliver_resume_book_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                },
                                success: function(data) {
                                    deliver_resume_book_dialog.html(data);
                                    post_delivery_cleanup();
                                }
                            });
                        } else {
                            show_form_submit_loader("#deliver_resume_book_form");
                            $("#deliver_resume_book_form input[type=submit]").attr("disabled", "disabled");
                            var download_url = RESUME_BOOK_CURRENT_DOWNLOAD_URL + "?resume_book_id=" + that.attr("data-resume-book-id") 
                                                                                + "&delivery_type=" + delivery_type;
                            if (custom_resume_book_name){ download_url = download_url + "&name=" + escape(custom_resume_book_name) }
                            window.location.href = download_url;
                            setTimeout(function(){
                                $.ajax({
                                    dataType: "html",
                                    url: RESUME_BOOK_CURRENT_DELIVERED_URL,
                                    error: function(jqXHR, textStatus, errorThrown) {
                                        if(jqXHR.status==0){
                                            deliver_resume_book_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                        }else{
                                            deliver_resume_book_dialog.html(ERROR_MESSAGE_DIALOG);
                                        }
                                    },
                                    success: function (data) {
                                        deliver_resume_book_dialog.html(data);
                                        deliver_resume_book_dialog.dialog('option', 'title', 'Resume Book Delivered Successfully');
                                    }
                                });
                                post_delivery_cleanup();
                            }, 1000);
                        }
                    } else {
                        $("#deliver_resume_book_form .error_section").html("Please wait until the resume book is ready.");
                    }
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    delivery_type: {
                        required: true
                    }
                }
            });
            recreate_resume_file();
        }
    });
};
$(document).ready(function(){
    $('.deliver_resume_book_link').click(handle_deliver_resume_book_link_click);
});