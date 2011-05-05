/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
*/

$(document).ready( function() {
    var languages_max = 12;
    var campus_org_max = 12;
    var industries_of_interest_max = 12;
    var previous_employers_max = 12;
   
        
    function open_create_campus_organization_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Campus Organization",
            dialogClass: "create_campus_organization_dialog",
            modal:true,
            width:480,
            resizable: false,
            close: function() {
                $create_campus_organization_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
	
	function open_create_language_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Language",
            dialogClass: "create_language_dialog",
            modal:true,
            width:500,
            resizable: false,
            close: function() {
                $create_language_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    function open_profile_form_info_dialog(){
        var $dialog = $('<div></div>')
        .dialog({
            autoOpen: false,
            title:"Why More Information is Better",
            dialogClass: "profile_form_info_dialog",
            modal:true,
            width:700,
            resizable: false
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    $('#create_campus_organization_link').click( function () {
        var $create_campus_organization_dialog = open_create_campus_organization_dialog();
        $create_campus_organization_dialog.html(ajax_loader);
        
        var create_campus_organization_dialog_timeout = setTimeout(show_loading_failed_message, 10000);
        $.ajax({
            dataType: "html",
            url: '/student/create-campus-organization/',
            success: function (data) {
                clearTimeout(create_campus_organization_dialog_timeout);
                
                $create_campus_organization_dialog.html(data);

                $("#id_type").multiselect({
                    noneSelectedText: "select campus organization type",
                    height:140,
                    header:false,
                    minWidth:187,
                    selectedList: 1,
                    multiple: false
                });
    
                format_required_labels("#create_campus_organization_form");
                align_form("#create_campus_organization_form", 20);
    
                var create_campus_organization_form_validator = $("#create_campus_organization_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#create_campus_organization_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"' + textStatus + '"</strong></div>';
                                error_message_details += close_dialog_link;
                                $create_campus_organization_dialog.html(error_message_template + error_message_details);
                            },
                            success: function(data) {
                                hide_form_submit_loader("#create_campus_organization_form");
                                switch(data.valid) {
                                    case true:
                                        var success_message = "<br><div class='message_section'><p>The listing for \"" + data.name + "\" has been created successfully!</p><br /><p><a class='select_new_campus_organization_link' href='javascript:void(0)'>Add to Profile & Close Dialog</a></p>";
                                        success_message += close_dialog_link;
                                        $create_campus_organization_dialog.html(success_message);
    
                                        // Add the new campus organization to the select and update the widget to include it
                                        $("optgroup[label=" + data.type + "s]").append('<option name="' + data.name + '" value="' + data.id + '">' + data.name + '</option>');
                                        $("#id_campus_orgs").multiselect("refresh");
                                        $("#id_campus_orgs").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
    
                                        // Marks the new campus org as selected on the actual select field, updates the widget, and then closes the dialog
                                        $(".select_new_campus_organization_link").click( function() {
                                            $("#id_campus_orgs").find('option[name="' + data.name + '"]').attr('selected', true);
                                            $("#id_campus_orgs").multiselect("refresh");
                                            $("#id_campus_orgs").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                            $create_campus_organization_dialog.dialog('destroy');
                                        });
                                        break;
                                    case false:
                                        var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"' + data.error.name + '"</strong></div>';
                                        error_message_details += close_dialog_link;
                                        $create_campus_organization_dialog.html(error_message_template + error_message_details);
                                        break;
                                    default:
                                        var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"Response status isn\'t valid."</strong></div>';
                                        error_message_details += close_dialog_link;
                                        $create_campus_organization_dialog.html(error_message_template + error_message_details);
                                        break;
                                }
                                $create_campus_organization_dialog.dialog('option', 'position', 'center');
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors,
                    rules: {
                        name: {
                            required: true,
                            remote: "/check-campus-organization-uniqueness"
                        },
                        type: {
                            required: true
                        },
                        website: {
                            remote: "/check-website"
                        }
                    },
                    messages:{
                        name:{
                            remote: "A campus organization with this name already exists"
                        },
                        website: "This url does not exist"
                    }
                });
            }
        });
    });
    
    $('#create_language_link').click( function () {
        
        $create_language_dialog = open_create_language_dialog();
        $create_language_dialog.html(ajax_loader);

        var create_language_dialog_timeout = setTimeout(show_loading_failed_message, 10000);
        $.ajax({
            dataType: "html",
            url: '/student/create-language/',
            success: function (data) {
                $create_language_dialog.html(data);
                
                clearTimeout(create_language_dialog_timeout);
                format_required_labels("#create_language_form");
                align_form("#create_language_form", 60);
    
                var create_language_form_validator = $("#create_language_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#create_language_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"' + textStatus + '"</strong></div>';
                                error_message_details += close_dialog_link;
                                $create_language_dialog.html(error_message_template + error_message_details);
                            },
                            success: function(data) {
                                hide_form_submit_loader("#create_language_form");
                                switch(data.valid) {
                                    case true:
                                        var success_message = "<br><div class='message_section'><p>The language \"" + data.name + "\" has been created successfully!</p><br />";
                                        success_message += "<p><a class='select_basic_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Basic)\" to Profile & Close Dialog</a></p><br />";
                                        success_message += "<p><a class='select_proficient_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Proficient)\" to Profile & Close Dialog</a></p><br />";
                                        success_message += "<p><a class='select_fluent_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Fluent)\" to Profile & Close Dialog</a></p><br />";
                                        success_message += close_dialog_link;
                                        $create_language_dialog.html(success_message);
    
                                        // Add the new campus organization to the select and update the widget to include it
                                        $("#id_languages").append('<option name="' + data.name + ' (Basic)" value="' + data.basic_id + '">' + data.name + ' (Basic)</option>');
                                        $("#id_languages").append('<option name="' + data.name + ' (Proficient)" value="' + data.proficient_id + '">' + data.name + ' (Proficient)</option>');
                                        $("#id_languages").append('<option name="' + data.name + ' (Fluent)" value="' + data.fluent_id + '">' + data.name +  ' (Fluent)</option>');
                                        $("#id_languages").multiselect("refresh");
                                        $("#id_languages").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
    
                                        // Marks the basic version of the language as selected on the actual select field, updates the widget, and then closes the dialog
                                        $(".select_basic_language_link").click( function() {
                                            $("#id_languages").find('option[name="' + data.name + ' (Basic)"]').attr('selected', true);
                                            $("#id_languages").multiselect("refresh");
                                            $create_language_dialog.dialog('destroy');
                                        });
                                        // Marks the proficient version of the language as selected on the actual select field, updates the widget, and then closes the dialog
                                        $(".select_proficient_language_link").click( function() {
                                            $("#id_languages").find('option[name="' + data.name + ' (Proficient)"]').attr('selected', true);
                                            $("#id_languages").multiselect("refresh");
                                            $create_language_dialog.dialog('destroy');
                                        });
                                        // Marks the fluent version of the language as selected on the actual select field, updates the widget, and then closes the dialog
                                        $(".select_fluent_language_link").click( function() {
                                            $("#id_languages").find('option[name="' + data.name + ' (Fluent)"]').attr('selected', true);
                                            $("#id_languages").multiselect("refresh");
                                            $create_language_dialog.dialog('destroy');
                                        });
                                        break;
                                    case false:
                                        var error_message_details = "<div id=\"message_section\"><strong><br />Error Details</strong><br />\"" + data.error.name + "\"</strong></div>";
                                        error_message_details += close_dialog_link;
                                        $create_language_dialog.html(error_message_template + error_message_details);
                                        break;
                                    default:
                                        var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"Response status isn\'t valid."</strong></div>';
                                        error_message_details += close_dialog_link;
                                        $create_language_dialog.html(error_message_template + error_message_details);
                                        break;
                                }
                                $create_language_dialog.dialog('option', 'position', 'center');
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors,
                    rules: {
                        name: {
                            required: true,
                            remote: "/check-language-uniqueness"
                        },
                    },
                    messages:{
                        name:{
                            remote: "This language already exists"
                        },
                    }
                });
            }
        });
    });

    $('#profile_form_info_link').click( function () {
        var $profile_form_info_dialog = open_profile_form_info_dialog();

        $profile_form_info_dialog.html(ajax_loader);
        $profile_form_info_dialog.load('/student/profile-form-info/', function () {
        });
    });
    // Create Profile Form Validation
    var v = $("#profile_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors_table,
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
            second_major: {
                notEqualTo : '#id_first_major'
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
                remote: "/check-website/"
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
            website: "This url does not exist.",
            resume: "Please select a PDF version of your resume.",
            second_major: "Second major must be different from first."
        }
    });

    // Get rid of resume field errors as a user selects a file
    // JQuery validation doesn't support the change event
    $("#id_resume").change( function() {
        v.element("#id_resume");
    });

    $("#id_school_year").multiselect({
        noneSelectedText: "select school year",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        header:false,
        minWidth:310,
        height:140,
        selectedList: 1,
        multiple: false,
        close: function(e) {
            if( $(this).multiselect("widget").find("input:checked").length > 0 ) {
                v.element("#id_school_year");
            }
        },
    });

    $("#id_graduation_year").multiselect({
        noneSelectedText: "select graduation year",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        header:false,
        selectedList: 1,
        height:117,
        minWidth:310,
        multiple: false,
        close: function(e) {
            if( $(this).multiselect("widget").find("input:checked").length > 0 ) {
                v.element("#id_graduation_year");
            }
        },
    });

    $("#id_first_major").multiselect({
        noneSelectedText: "select first major",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        height:140,
        header:false,
        minWidth:310,
        selectedList: 1,
        multiple: false,
        close: function(e) {
            if( $(this).multiselect("widget").find("input:checked").length > 0 ) {
                v.element("#id_first_major");
            }
        },
    });

    $("#id_second_major").multiselect({
        noneSelectedText: "select second major",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        height:140,
        header:false,
        minWidth:310,
        selectedList: 1,
        multiple: false
    });

    $("#id_looking_for").multiselect({
        noneSelectedText: "select",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("#id_older_than_18").multiselect({
        noneSelectedText: "select",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("#id_citizen").multiselect({
        noneSelectedText: "select",
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("#id_languages").multiselect({
        noneSelectedText: 'select languages',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        minWidth:310,
        height:170,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            if( $(this).multiselect("widget").find("input:checked").length > languages_max ) {
                show_multiselect_warning("id_languages", languages_max);
                return false;
            }
        }
    }).multiselectfilter();

    $("#id_campus_orgs").multiselect({
        noneSelectedText: 'select campus organizations',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        minWidth:310,
        height:230,
        optgrouptoggle: function(e, ui) {
            $(".warning").remove();
            if (ui.inputs.length + $(this).multiselect("widget").find("input:checked").length > campus_org_max) {
                show_multiselect_warning("id_campus_orgs", campus_org_max);
                return false;
            }
        },
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            if( $(this).multiselect("widget").find("input:checked").length > campus_org_max ) {
                show_multiselect_warning("id_campus_orgs", campus_org_max);
                return false;
            }
        }
    }).multiselectfilter();

    $("#id_industries_of_interest").multiselect({
        noneSelectedText: 'select industries',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        minWidth:310,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            if( $(this).multiselect("widget").find("input:checked").length > industries_of_interest_max ) {
                show_multiselect_warning("id_industries_of_interest", industries_of_interest_max);
                return false;
            }
        }
    }).multiselectfilter();

    $("#id_previous_employers").multiselect({
        noneSelectedText: 'select employers',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
        minWidth:310,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            if( $(this).multiselect("widget").find("input:checked").length > previous_employers_max ) {
                show_multiselect_warning("id_previous_employers", previous_employers_max);
                return false;
            }
        }
    }).multiselectfilter();
    
    // Set up multipart form navigation
    $(".navigation").click( function() {
        if (current < this.id) {
            if (v.form()) {
                accordion.accordion("activate", parseInt(this.id));
                current = parseInt(this.id);
            }
        } else {
            accordion.accordion("activate", parseInt(this.id));
            current = parseInt(this.id);
        }
    });
    // Back buttons do not need to run validation
    $("#pg2 .open0").click( function() {
        accordion.accordion("activate", 0);
        current = 0;
    });
    $("#pg3 .open1").click( function() {
        accordion.accordion("activate", 1);
        current = 1;
    });
    $("#pg4 .open2").click( function() {
        accordion.accordion("activate", 2);
        current = 2;
    });
    
    // Next buttons need to run validation
    $("#pg3 .open3").click( function() {
        if (v.form()) {
            accordion.accordion("activate", 3);
            current = 3;
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

    // Set up accordion and validation
    var current = 0;  // Current Page
    var accordion = $("#stepForm").accordion({
        autoHeight:false,
        animated:false
    });
    accordion.accordion( "option", "active", parseInt(get_parameter_by_name("page")));
    
    // Field masks
    $("#id_act").mask("99",{placeholder:" "}).blur( function() {
        if($(this).val()=="") {
            $("#act .error").remove();
        }
    });
    $("#id_sat_v").mask("999",{placeholder:" "}).blur( function() {
        if($(this).val()=="") {
            $("#sat_v .error").remove();
        }
    });
    $("#id_sat_m").mask("999",{placeholder:" "}).blur( function() {
        if($(this).val()=="") {
            $("#sat_m .error").remove();
        }
    });
    $("#id_sat_w").mask("999",{placeholder:" "}).blur( function() {
        if($(this).val()=="") {
            $("#sat_w .error").remove();
        }
    });
});