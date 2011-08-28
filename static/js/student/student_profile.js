$(document).ready( function() {
    
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
                        $("#student_profile_preview").html(data);

                        $(".student_checkbox").tipsy({'gravity':'e', opacity: 0.9, fallback:PREVIEW_CHECKBOX_TOOLTIP, html:true});

                        $(".resume_book_current_toggle_student").hover(function(){
                            $($(this).children()[0]).removeClass("sprite-plus").addClass("sprite-cross");    
                        }, function(){
                            $($(this).children()[0]).removeClass("sprite-cross").addClass("sprite-plus");     
                        }).tipsy({'gravity':'e', opacity: 0.9, title:function(){return resume_book_current_toggle_tooltip;}, html:true});
                        
                        $(".student_toggle_star").hover(function(){
                            $($(this).children()[0]).removeClass("sprite-star-empty").addClass("sprite-star");    
                        }, function(){
                            $($(this).children()[0]).removeClass("sprite-star").addClass("sprite-star-empty");   
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
            }
        }else{
            clearTimeout(profile_preview_timeout);
            $("#student_profile_preview").html(FILL_OUT_REQUIRED_FIELDS_MESSAGE);
        }
    };
    v = $("#profile_form").validate({
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
                        }else{
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
            first_name: FIRST_NAME_REQUIRED,
            last_name: LAST_NAME_REQUIRED,
            school_year: SCHOOL_YEAR_REQUIRED,
            graduation_year: GRADUATION_YEAR_REQUIRED,
            first_major: FIRST_MAJOR_REQUIRED,
            gpa: {
                required: GPA_REQUIRED,
                range: GPA_RANGE
            },
            resume: RESUME_REQUIRED,
            website: INVALID_URL
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
    // The setup of the mask MUST come after the formating of the number above
    $("#id_gpa").mask("9.99",{placeholder:" "});
        
    $("#pg2 .open0").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 0);
            current = 0;
        }
    });
    $("#pg3 .open1").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 1);
            current = 1;
        }
    });
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
   
    $("#profile_form select, #profile_form input[type=file]").live('change', load_profile_preview);
    var timeoutID;
    $('#profile_form input[type=text]').keydown(function(e) {
        if(e.which != 9) {
            if( typeof timeoutID != 'undefined')
                window.clearTimeout(timeoutID);
            timeoutID = window.setTimeout(load_profile_preview, 400);
        }
    });

    $("#student_profile_preview").html(PREVIEW_AJAX_LOADER);
    var profile_preview_timeout = setTimeout(function(){$("#student_profile_preview_ajax_loader p").html(single_line_long_load_message);}, LOAD_WAIT_TIME);
    load_profile_preview();
});