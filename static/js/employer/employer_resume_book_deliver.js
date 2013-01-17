var resume_book_created, delivery_type, delivery_format, custom_resume_book_name, that;

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
        if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
            initiate_ajax_call();
        }
        update_resume_book_contents_summary();
        $(".resume_book_toggle_student").html(ADD_TO_RESUME_BOOK_IMG);
    }
}

function recreate_resume_file() {
    resume_book_created = false;
    $("#deliver_resume_book_form_loader").css('display','inline');
    $.ajax({
        type: "POST",
        data:{'delivery_format':delivery_format,'resume_book_id':that.attr("data-resume-book-id")},
        dataType: "json",
        url: RESUME_BOOK_CREATE_URL,
        error: function(jqXHR, textStatus, errorThrown) {
            errors_in_dialog_error_section("deliver_resume_book_dialog", jqXHR, textStatus, errorThrown);
        },
        success: function (data) {
            resume_book_created = true;
            $("#deliver_resume_book_form_loader").css('display','none');
        }
    });
}

function download_resume_book(){
    // Show the loader and disable submit button
    show_form_submit_loader("#deliver_resume_book_form");
    $("#deliver_resume_book_form input[type=submit]").attr("disabled", "disabled");
    
    // Create the submission url
    var download_url = RESUME_BOOK_DOWNLOAD_URL;
    download_url += "?resume_book_id=" + that.attr("data-resume-book-id") 
    download_url += "&delivery_format=" + delivery_format;
    
    // Add custom name, if provided
    if (custom_resume_book_name){
        download_url = download_url + "&name=" + escape(custom_resume_book_name);
    }
    
    // Download the file
    downloadURL(download_url);
    //window.location.href = download_url;
    
    // Show success message after 1 second
    setTimeout(function(){
        $.ajax({
            dataType: "html",
            url: RESUME_BOOK_DELIVERED_URL,
            error: function(jqXHR, textStatus, errorThrown) {
                errors_in_dialog_error_section("deliver_resume_book_dialog", jqXHR, textStatus, errorThrown);
            },
            success: function (data) {
                deliver_resume_book_dialog.html(data);
                deliver_resume_book_dialog.dialog('option', 'title', 'Resume Book Delivered Successfully');
            }
        });
        post_delivery_cleanup();
    }, 1000);
}

function handle_resume_book_deliver_link_click() {
    delivery_type = 'download';
    delivery_format = 'combined';
    custom_resume_book_name = "";
    resume_book_created = false;
    that = null;
    
    deliver_resume_book_dialog = open_deliver_resume_book_dialog();
    deliver_resume_book_dialog.html(DIALOG_AJAX_LOADER);
    that = $(this);
    
    var deliver_resume_book_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        data: {'resume_book_id':that.attr("data-resume-book-id")},
        dataType: "html",
        url: RESUME_BOOK_DELIVER_URL,
        complete: function(jqXHR, textStatus) {
            clearTimeout(deliver_resume_book_dialog_timeout);
            deliver_resume_book_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            errors_in_dialog_error_section("deliver_resume_book_dialog", jqXHR, textStatus, errorThrown);
        },
        success: function (data) {
            deliver_resume_book_dialog.html(data);
            // Mark the emails field as required visually
            // It had to be left as optional in case the user wantd to download.
            // If it was required the form would not validate with this field being empty
            $("label[for=id_emails]").addClass('required').append("<span class='error'>*</span>");
            
            $("#id_emails").autoResize({
                animateDuration : 0,
                extraSpace : 18
            }).live('blur', function(){
                $(this).height(this.offsetHeight-28); 
            });

            $("#delivery_formats li").click(function(){
                if($(this).attr("class")!="disabled"){
                    $(this).parent().children().removeClass("selected");
                    $(this).addClass("selected");
                    delivery_format = $(this).data("delivery-format");
                    recreate_resume_file();
                }
            });

            $("#delivery_types li").click(function(){
                if(!$(this).hasClass("disabled")){
                    $(this).parent().children().removeClass("selected");
                    $(this).addClass("selected");
                    delivery_type = $(this).data("delivery-type");
                    if (delivery_type == "email") {
                        // Delivery format an only be "combined"
                        delivery_format = "combined";
                        $(".email_delivery_type_only_field").show()
                        $("#id_emails").rules("add", {
                            multiemail: true,
                            required: true
                        });
                        $("#deliver_resume_book_form_submit_button").val("Email");
    
                        $("#delivery_formats li").removeClass("selected");
                        $("#delivery_formats li").filter(function(){ return $(this).data("delivery-format")=="separate";}).addClass("disabled");
                        $("#delivery_formats li").filter(function(){ return $(this).data("delivery-format")=="combined";}).addClass("selected");
                        recreate_resume_file();
                    } else {
                        $("#delivery_formats li").filter(function(){ return $(this).data("delivery-format")=="separate";}).removeClass("disabled");
                        $(".email_delivery_type_only_field").hide();
                        $("#id_emails").rules("remove", "email required");
                        $("#deliver_resume_book_form_submit_button").val("Download");
                    }
                }
            });

            
            var deliver_resume_book_form_validator = $("#deliver_resume_book_form").validate({
                submitHandler: function(form) {
                    if(resume_book_created) {
                        custom_resume_book_name = $("#id_name").val();
                        $("#deliver_resume_book_form .error_section").html("");
                        if(delivery_type=="email") {
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
                                    errors_in_dialog_error_section("deliver_resume_book_dialog", jqXHR, textStatus, errorThrown);
                                },
                                success: function(data) {
                                    deliver_resume_book_dialog.html(data);
                                    post_delivery_cleanup();
                                }
                            });
                        } else {
                            download_resume_book();
                        }
                    } else {
                        $("#deliver_resume_book_form .error_section").html("Please wait until the resume book is ready.");
                    }
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error
            });
            recreate_resume_file();
        }
    });
};

$(document).ready(function(){
    $('.resume_book_deliver_link').live('click', handle_resume_book_deliver_link_click);
});
