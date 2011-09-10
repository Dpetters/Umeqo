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


function handle_deliver_resume_book_link_click() {
    deliver_resume_book_dialog = open_deliver_resume_book_dialog();
    deliver_resume_book_dialog.html(DIALOG_AJAX_LOADER);
    var that = $(this);
    var resume_book_created = false;

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

            $("label[for=id_emails]").addClass('required');
            $("#id_emails").autoResize({
                animateDuration : 0,
                extraSpace : 18
            }).live('blur', function(){
                $(this).height(this.offsetHeight-28); 
            });
            
            $("#id_delivery_type").multiselect({
                noneSelectedText: "select delivery type",
                height:53,
                header:false,
                minWidth:200,
                selectedList: 1,
                multiple: false,
                click: function(event, ui) {
                    if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                        $('.email_delivery_type_only_field').show()
                        $('#id_emails').rules("add", {
                            multiemail: true,
                            required: true
                        });
                        $("#deliver_resume_book_form_submit_button").val("Email");
                    } else {
                        $('.email_delivery_type_only_field').hide();
                        $('#id_emails').rules("remove", "email required");
                        $("#deliver_resume_book_form_submit_button").val("Download");
                    }
                }
            });
            var deliver_resume_book_form_validator = $("#deliver_resume_book_form").validate({
                submitHandler: function(form) {
                    if(resume_book_created) {
                        var custom_resume_book_name = $("#id_name").val();
                        $("#deliver_resume_book_form .error_section").html("");
                        if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                            console.log(that.attr("data-resume-book-id"));
                            console.log(that);
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
                                }
                            });
                        } else {
                            show_form_submit_loader("#deliver_resume_book_form");
                            $("#deliver_resume_book_form input[type=submit]").attr("disabled", "disabled");
                            console.log(that.attr("data-resume-book-id"));
                            console.log(that);
                            var download_url = RESUME_BOOK_CURRENT_DOWNLOAD_URL + "?resume_book_id=" + that.attr("data-resume-book-id");
                            console.log(download_url);
                            if (custom_resume_book_name){ download_url = download_url + "?name=" + escape(custom_resume_book_name) }
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
                            }, 500);
                        }
                        if(typeof(ADD_TO_RESUME_BOOK_IMG)!="undefined"){
                            $(".resume_book_current_toggle_student").html(ADD_TO_RESUME_BOOK_IMG);
                            $("#students_in_resume_book_num").text("0")
                            $(".student_deliver_resume_book_link").attr("disabled", "disabled");
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
            $.ajax({
                type: "POST",
                data:{'resume_book_id':that.attr("data-resume-book-id")},
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
                    $("#resume_book_status").html("Ready");
                    $("#resume_book_status").addClass('ready');
                    $("#resume_book_status").removeClass('error');                        
                }
            });
        }
    });
};
$(document).ready(function(){
    $('.student_deliver_resume_book_link').click(handle_deliver_resume_book_link_click);
});