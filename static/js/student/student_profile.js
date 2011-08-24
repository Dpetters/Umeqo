$(document).ready( function() {
    var v = $("#profile_form").validate({
        submitHandler: function (form) {
            $(form).ajaxSubmit({
                dataType: 'text',
                beforeSubmit: function (arr, $form, options) {
                    $("#profile_form input[type=submit]").attr("disabled", "disabled");
                    show_form_submit_loader("#profile_form");
                    $("#profile_form .error_section").html("");
                },
                complete : function(jqXHR, textStatus) {
                    $("#profile_form input[type=submit]").removeAttr("disabled");
                    hide_form_submit_loader("#profile_form");
                },
                success: function (data) {
                    console.log("HERE");
                    console.log(data);
                    data = $.parseJSON(data);
                    if(data.valid) {
                        window.location.href = HOME_URL + "?msg=profile-saved";
                    } else {
                          if(data.unparsable_resume){
                            var $unparsable_resume_dialog = open_unparsable_resume_dialog();
                            $unparsable_resume_dialog.html(DIALOG_AJAX_LOADER);
                            $unparsable_resume_dialog.dialog('option', 'position', 'center');
                            var unparsable_resume_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
                            $.ajax({
                                dataType: "html",
                                url: UNPARSABLE_RESUME_URL,
                                complete: function(jqXHR, textStatus) {
                                    clearTimeout(unparsable_resume_dialog_timeout);
                                },
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $unparsable_resume_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                        $unparsable_resume_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                },
                                success: function (data) {
                                    $unparsable_resume_dialog.html(data);
                                    $unparsable_resume_dialog.dialog('option', 'position', 'center');
                                    $(".choose_another_resume_link").live('click', function(){
                                        $unparsable_resume_dialog.remove();
                                           accordion.accordion("activate", 0);
                                        current = 0;
                                        $("#id_resume").focus();
                                    });
                                    $(".save_profile_link").live('click', function(){
                                        window.location.href = HOME_URL + "?msg=profile-saved";
                                    });
                                }
                            });
                       } else{
                            if('second_major' in data.errors){
                                   accordion.accordion("activate", 1);
                                current = 1;
                            }
                            place_table_form_errors("#profile_form", data.errors);
                        }
                    }
                },
                error: errors_in_message_area_handler
            });
        },
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_table_form_field_error,
        rules: {
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            school_year: {
                required: true
            },
            graduation_year: {
                required: true
            },
            first_major: {
                required: true
            },
            gpa: {
                required: true,
                range: [0, 5.0],
                maxlength: 4
            },
            resume:{
                accept: "pdf"
            },
            website:{
                complete_url: true
            },
            sat_m: {
                range: [200, 800],
                maxlength: 3
            },
            sat_w: {
                range: [200, 800],
                maxlength: 3
            },
            sat_v: {
                range: [200, 800],
                maxlength: 3
            },
            act: {
                range: [0, 36],
                maxlength: 2
            }
        },
        messages: {
            first_name: STUDENT_PROFILE_FORM_FIRST_NAME,
            last_name: STUDENT_PROFILE_FORM_LAST_NAME,
            school_year: STUDENT_PROFILE_FORM_SCHOOL_YEAR,
            graduation_year: STUDENT_PROFILE_FORM_GRADUATION_YEAR,
            first_major: STUDENT_PROFILE_FORM_FIRST_MAJOR,
            gpa: {
                required: STUDENT_PROFILE_FORM_GPA_REQUIRED,
                range: STUDENT_PROFILE_FORM_GPA_RANGE
            },
            resume: STUDENT_PROFILE_FORM_RESUME,
            website: invalid_url
        }
    });

    // Get rid of resume field errors as a user selects a file
    // JQuery validation doesn't respond to the change event
    $("#id_resume").change( function() {
        v.element("#id_resume");
    });  
    
    $("#id_gpa").blur(function(){
        $("#id_gpa").val(formatNumber($("#id_gpa").val(),2,' ','.','','','-','').toString());
    });
    // Also just do this on load so that the value from Django (2.3 for example)
    // escapes validation and becomes 2.30.
    if($("#id_gpa").val()){
        $("#id_gpa").val(formatNumber($("#id_gpa").val(),2,' ','.','','','-','').toString());
    }
    
    // Back buttons do not need to run validation
    $("#pg2 .open0").click( function() {
        accordion.accordion("activate", 0);
        current = 0;
    });
    $("#pg3 .open1").click( function() {
        accordion.accordion("activate", 1);
        current = 1;
    });
    
    // Next buttons need to run validation
    $("#pg2 .open2").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 2);
            current = 2;
        }
    });
    $("#pg1 .open1").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 1);
            current = 1;
        }
    });
    
    $("#id_gpa").mask("9.99",{placeholder:" "});
    
    $("#profile_file select, #profile_form input[type=text], #profile_file input[type=file]").live('change', load_profile_preview);
    
    function load_profile_preview(){
        var required_fields_filled_out = true;
        $("label.required").each(function(){
            required_fields_filled_out = required_fields_filled_out && $("#" + $(this).attr("for")).val();
        });
        if(required_fields_filled_out){
            if ($("#profile_form").valid()){
                var student_detailed_info_visible = $(".student_detailed_info").is(":visible");
                $("#profile_form").ajaxSubmit({
                    type:"POST",
                    dataType: "html",
                    url: PROFILE_PREVIEW_URL,
                    iframe: false,
                    complete: function(jqXHR, textStatus) {
                        clearTimeout(profile_preview_timeout);
                    },
                    error: errors_in_message_area_handler,
                    success: function (data) { 
                        $("#listing_preview").html(data);
                        $(".student_checkbox").tipsy({'gravity':'e', opacity: 0.9, fallback:STUDENT_PROFILE_PREVIEW_CHECKBOX_TOOLTIP, html:true});
                        $(".resume_book_current_toggle_student").hover(function(){
                            $(this).html(REMOVE_FROM_RESUME_BOOK_IMG);    
                        }, function(){
                            $(this).html(ADD_TO_RESUME_BOOK_IMG);    
                        }).tipsy({'gravity':'e', opacity: 0.9, title:function(){return resume_book_current_toggle_tooltip;}, html:true});
                        $(".student_toggle_star").hover(function(){
                            $(this).html(STARRED_IMG);    
                        }, function(){
                            $(this).html(UNSTARRED_IMG);    
                        }).tipsy({'gravity':'e', opacity: 0.9, fallback:star_toggle_tooltip, html:true});
                        $(".student_event_attendance").tipsy({'gravity':'w', opacity: 0.9, fallback:event_attendance_tooltip, html:true});
                        if (student_detailed_info_visible){
                            $(".student_toggle_detailed_info_link").html(HIDE_DETAILS_LINK);
                            $(".student_detailed_info").show();
                        }else{
                            $(".student_detailed_info").hide();
                        }
                        $(".student_invite_to_event_link").tipsy({'gravity':'e', opacity: 0.9, fallback:invite_to_event_tooltip, html:true});
                        $(".student_resume_link").tipsy({'gravity':'e', opacity: 0.9, fallback:view_resume_tooltip, html:true});
                        $(".student_comment").autoResize({
                            animateDuration : 0,
                            extraSpace : 18
                        });
                    }
                });
            }else{
                $("#listing_preview").html(data);
            }
        }else{
            clearTimeout(profile_preview_timeout);
            $("#listing_preview").html(FILL_OUT_REQUIRED_FIELDS_MESSAGE);
        }
    };
    $("#listing_preview").html(STUDENT_PROFILE_PREVIEW_AJAX_LOADER);
    var profile_preview_timeout = setTimeout(function(){$("#student_profile_preview_ajax_loader p").html(single_line_long_load_message);}, LOAD_WAIT_TIME);
    load_profile_preview();
});