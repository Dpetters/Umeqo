$(document).ready( function() {
    var languages_max = 12;
    var campus_involvement_max = 12;
    var industries_of_interest_max = 12;
    var previous_employers_max = 12;
    var countries_of_citizenship_max = 3;
    
    var create_campus_organization_dialog = null;
    var create_language_dialog = null;
        
    function open_create_campus_organization_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Campus Organization",
            dialogClass: "create_campus_organization_dialog",
            modal:true,
            width:475,
            resizable: false,
            close: function() {
                create_campus_organization_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    function open_create_language_dialog() {
        var dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Language",
            dialogClass: "create_language_dialog",
            modal:true,
            width:475,
            resizable: false,
            close: function() {
                create_language_dialog.remove();
            }
        });
        dialog.dialog('open');
        return dialog;
    };

    function open_unparsable_resume_dialog(){
        var dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Unparsable Resume",
            dialogClass: "unparsable_resume_dialog",
            modal:true,
            width:410,
            resizable: false,
            close: function() {
                $unparsable_resume_dialog.remove();
            }
        });
        dialog.dialog('open');
        return dialog;
	};
	
    $('#create_campus_organization_link').click( function () {
        create_campus_organization_dialog = open_create_campus_organization_dialog();
        create_campus_organization_dialog.html(dialog_ajax_loader);
        
        var create_campus_organization_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CREATE_CAMPUS_ORGANIZATION_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_campus_organization_dialog_timeout);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
					create_campus_organization_dialog.html(dialog_check_connection_message);
				}else{
                    create_campus_organization_dialog.html(dialog_error_message);
                }
            },
            success: function (data) {             
                create_campus_organization_dialog.html(data);
                create_campus_organization_dialog.dialog('option', 'position', 'center');
                
                $("#id_name").focus();
                
                var create_campus_org_form_validator = $("#create_campus_org_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#create_campus_org_form");
                            },
                            complete: function(jqXHR, textStatus) {
                                hide_form_submit_loader("#create_campus_org_form");
				            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_campus_organization_dialog .error_section").html(form_check_connection_message);
                                }else{
                                    create_campus_organization_dialog.html(dialog_error_message);
                                }
                                create_campus_organization_dialog.dialog('option', 'position', 'center');
                            },
                            success: function(data) {
                                if (data.valid) {
                                    var success_message = "<br><div class='message_section'><p>The listing for \"" + data.name + "\" has been created successfully!</p><br /><p><a class='select_new_campus_organization_link' href='javascript:void(0)'>Add it to your Campus Involvement  & Close Dialog</a></p>";
                                    success_message += CLOSE_DIALOG_LINK
                                    create_campus_organization_dialog.html(success_message);

                                    // Add the new campus organization to the select and update the widget to include it
                                    $("optgroup[label='" + data.type + "s']").append('<option name="' + data.name + '" value="' + data.id + '">' + data.name + '</option>');
                                    $("#id_campus_involvement").multiselect("refresh");
                                    $("#id_campus_involvement").multiselect("widget").find(".ui-multiselect-optgroup-label").show();

                                    // Marks the new campus org as selected on the actual select field, updates the widget, and then closes the dialog
                                    $(".select_new_campus_organization_link").click( function() {
                                        $("#id_campus_involvement").find('option[name="' + data.name + '"]').attr('selected', true);
                                        $("#id_campus_involvement").multiselect("refresh");
                                        $("#id_campus_involvement").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                    });
								}else{
									place_table_form_errors("#create_campus_org_form", data.errors);
                                }
                                create_campus_organization_dialog.dialog('option', 'position', 'center');
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors_table,
                    rules: {
                        name: {
                            required: true,
                            remote: {
                                url: CHECK_CAMPUS_ORGANIZATION_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".create_campus_organization_dialog .error_section").html(form_check_connection_message);
                                    }else{
                                        create_campus_organization_dialog.html(dialog_error_message);
                                    }
                                	create_campus_organization_dialog.dialog('option', 'position', 'center');
                                },
                            }
                        },
                        type: {
                            required: true
                        },
                        website: {
                            complete_url: true
                        }
                    },
                    messages:{
                        name:{
                            remote: "This campus organization already exists."
                        },
                    }
                });
            }
        });
    });
    
    
    
    
    $('#create_language_link').click( function () {
        
        create_language_dialog = open_create_language_dialog();
        create_language_dialog.html(dialog_ajax_loader);

        var create_language_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CREATE_LANGUAGE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_language_dialog_timeout);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
					create_campus_organization_dialog.html(dialog_check_connection_message);
				}else{
                    create_campus_organization_dialog.html(dialog_error_message);
                }
            },
            success: function (data) {             
                create_language_dialog.html(data);
                create_language_dialog.dialog('option', 'position', 'center');

                $("#id_name").focus();
                
                var create_language_form_validator = $("#create_language_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#create_language_form");
                            },
				            complete: function(jqXHR, textStatus) {
                                hide_form_submit_loader("#create_language_form");
				            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_language_dialog .error_section").html(form_check_connection_message);
                                }else{
                                    create_language_dialog.html(dialog_error_message);
                                }
                				create_language_dialog.dialog('option', 'position', 'center');
                            },
                            success: function(data) {
                                if(data.valid) {
                                    var success_message = "<div class='message_section'><p>The language \"" + data.name + "\" has been created successfully!</p>";
                                    success_message += "<p><a class='select_basic_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Basic)\" to your Languages & Close Dialog</a></p>";
                                    success_message += "<p><a class='select_proficient_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Proficient)\" to your Languages & Close Dialog</a></p>";
                                    success_message += "<p><a class='select_fluent_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Fluent)\" to your Language & Close Dialog</a></p>";
                                    success_message += CLOSE_DIALOG_LINK;
                                    create_language_dialog.html(success_message);

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
                                        create_language_dialog.dialog('destroy');
                                    });
                                    // Marks the proficient version of the language as selected on the actual select field, updates the widget, and then closes the dialog
                                    $(".select_proficient_language_link").click( function() {
                                        $("#id_languages").find('option[name="' + data.name + ' (Proficient)"]').attr('selected', true);
                                        $("#id_languages").multiselect("refresh");
                                        create_language_dialog.dialog('destroy');
                                    });
                                    // Marks the fluent version of the language as selected on the actual select field, updates the widget, and then closes the dialog
                                    $(".select_fluent_language_link").click( function() {
                                        $("#id_languages").find('option[name="' + data.name + ' (Fluent)"]').attr('selected', true);
                                        $("#id_languages").multiselect("refresh");
                                        create_language_dialog.dialog('destroy');
                                    });
								} else {
									place_table_form_errors("#create_language_form", data.errors);
                                }
                                create_language_dialog.dialog('option', 'position', 'center');
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors_table,
                    rules: {
                        name: {
                            required: true,
                            remote: {
                                url:CHECK_LANGUAGE_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".create_language_dialog .error_section").html(form_check_connection_message);
                                    }else{
                                        create_language_dialog.html(dialog_error_message);
                						create_language_dialog.dialog('option', 'position', 'center');
                                    }
                                },
                            }
                        },
                    },
                    messages:{
                        name:{
                            remote: "This language already exists."
                        },
                    }
                });
            }
        });
    });
    
    // Create Profile Form Validation
    var v = $("#profile_form").validate({
        submitHandler: function (form) {
            $(form).ajaxSubmit({
                dataType: 'text',
                beforeSubmit: function (arr, $form, options) {
                    show_form_submit_loader("#profile_form");
                },
                complete : function(jqXHR, textStatus) {              	
                	hide_form_submit_loader("#profile_form");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    if(jqXHR.status==0){
                        $("#profile_form .error_section").html(form_check_connection_message);
                    }else{
                    	show_error_dialog(page_error_message);
                    }
                },
                success: function (data) {
                	data = $.parseJSON(data);
                    if(data.valid) {
                    	window.location.href = HOME_URL + "?msg=profile-saved";
					} else {
					  	if(data.unparsable_resume){
							var $unparsable_resume_dialog = open_unparsable_resume_dialog();
						    $unparsable_resume_dialog.html(dialog_ajax_loader);
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
										$unparsable_resume_dialog.html(dialog_check_connection_message);
									}else{
						                $unparsable_resume.html(dialog_error_message);
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
					    }
					    else{
					    	if('id_second_major' in data.errors){
					   			accordion.accordion("activate", 1);
			            		current = 1;
			            	}
							place_table_form_errors("#profile_form", data.errors);
					    }
                   }
                }
            });
        },
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
            gpa: {
                required: true,
                range: [0, 5.0],
                maxlength: 4
            },
            resume:{
                accept: "pdf"
            },
            website:{
                complete_url: true,
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
            website: STUDENT_PROFILE_FORM_WEBSITE
        }
    });

    // Get rid of resume field errors as a user selects a file
    // JQuery validation doesn't respond to the change event
    $("#id_resume").change( function() {
        v.element("#id_resume");
    });

    $("#id_looking_for").multiselect({
        noneSelectedText: 'select job types',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        click: function(){
        	$("#id_looking_for").trigger("change");
        },
        checkAll: function(){
        	$("#id_looking_for").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_looking_for").trigger("change");
        },
    }).multiselectfilter();    
	
    $("#id_gpa").blur(function(){
        $("#id_gpa").val(formatNumber($("#id_gpa").val(),2,' ','.','','','-','').toString());
    });
    // Also just do this on load so that the value from Django (2.3 for example)
    // escapes validation and becomes 2.30.
    if($("#id_gpa").val()){
    	$("#id_gpa").val(formatNumber($("#id_gpa").val(),2,' ','.','','','-','').toString());
	}
	
    $("#id_industries_of_interest").multiselect({
        noneSelectedText: 'select industries',
        classes: 'interested_in_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            $("#id_industries_of_interest").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > industries_of_interest_max ) {
                place_multiselect_warning_table($("#id_industries_of_interest"), industries_of_interest_max);
                return false;
            }
        },
        checkAll: function(){
        	$("#id_industries_of_interest").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_industries_of_interest").trigger("change");
        },
    }).multiselectfilter();

    $("#id_previous_employers").multiselect({
        noneSelectedText: 'select employers',
        classes: 'previous_employers_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
        	$("#id_previous_employers").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > previous_employers_max ) {
                place_multiselect_warning_table($("#id_previous_employers"), previous_employers_max);
                return false;
            }
        },
        checkAll: function(){
        	$("#id_previous_employers").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_previous_employers").trigger("change");
        },
    }).multiselectfilter();

    $("#id_campus_involvement").multiselect({
        noneSelectedText: 'select campus organizations',
        classes: 'campus_involvement_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        beforeoptgrouptoggle: function(e, ui){
            $(".warning").remove();
            if( ui.inputs.length - $(ui.inputs).filter(':checked').length + $(this).multiselect("widget").find("input:checked").length > campus_involvement_max ) {
                place_multiselect_warning_table($("#id_campus_involvement"), campus_involvement_max);
                return false;
            }
        },
        minWidth:multiselectMinWidth,
        height:146,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e, ui) {
            $(".warning").remove();
            $("#id_campus_involvement").trigger("change");
            if( ui.checked && $(this).multiselect("widget").find("input:checked").length > campus_involvement_max ) {
                place_multiselect_warning_table($("#id_campus_involvement"), campus_involvement_max);
                return false;
            }
        },
        checkAll: function(){
        	$("#id_campus_involvement").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_campus_involvement").trigger("change");
        },
    }).multiselectfilter();
    
    $("#id_languages").multiselect({
        noneSelectedText: 'select languages',
        classes: 'languages_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        height:146,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(event, ui) {
            $(".warning").remove();
            $("#id_languages").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > languages_max ) {
                place_multiselect_warning_table($("#id_languages"), languages_max);
                return false;
            }
            var num = $(this).multiselect("widget").find("input:checked").filter(function(){
            	 if(this.title.split(' (')[0] == ui.text.split(' (')[0])
            	 	return true;
           	}).length;
           	if (num > 1){
           		place_errors_table($("<label class='warning' for'" + $("#id_languages").attr("id") + "'>You can only select one language difficulty.</label>"), $("#id_languages"));
           		return false;
           	}
        },
        checkAll: function(){
        	$("#id_languages").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_languages").trigger("change");
        },
    }).multiselectfilter();

    $("#id_countries_of_citizenship").multiselect({
        noneSelectedText: "select countries",
        classes: 'countries_of_citizenship_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        height:146,
        minWidth:multiselectMinWidth,
        selectedList: 1,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            $("#id_countries_of_citizenship").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > countries_of_citizenship_max ) {
                place_multiselect_warning_table($("#id_countries_of_citizenship"), countries_of_citizenship_max);
                return false;
            }
        },
        checkAll: function(){
        	$("#id_countries_of_citizenship").trigger("change");
        },
        uncheckAll: function(){
        	$("#id_countries_of_citizenship").trigger("change");
        },
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

    // Set up accordion and validation
    var current = 0;  // Current Page
    accordion = $("#stepForm").accordion({
        autoHeight:false,
        animated:false
    });
    accordion.accordion( "option", "active", parseInt(get_parameter_by_name("page")));
    
    // Field masks
    $("#id_gpa").mask("9.99",{placeholder:" "});
    
    $("select, input[type=text], input[type=file]").live('change', load_profile_preview);
    
    
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
			        error: function(jqXHR, textStatus, errorThrown) {
		                if(jqXHR.status==0) {
		                    show_error_dialog(page_check_connection_message);
						}else{
		                    show_error_dialog(page_error_message);
		                }
			        },
			        success: function (data) { 
			        	$("#listing_preview").html(data);
			        	if (student_detailed_info_visible){
			        		$(".student_toggle_detailed_info_link").html(HIDE_DETAILS_LINK);
			        		$(".student_detailed_info").show();
			        	}else{
			        		$(".student_detailed_info").hide();
			        	}
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