$(document).ready( function() {
	var create_language_dialog = null;
    
    function open_create_language_dialog() {
        var dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Language",
            dialogClass: "create_language_dialog",
            modal:true,
            width:480,
            resizable: false,
            close: function() {
                create_language_dialog.remove();
            }
        });
        dialog.dialog('open');
        return dialog;
    };
    
    $('#create_language_link').click( function () {
        
        create_language_dialog = open_create_language_dialog();
        create_language_dialog.html(DIALOG_AJAX_LOADER);

        var create_language_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CREATE_LANGUAGE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_language_dialog_timeout);
                create_language_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
					create_language_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
				}else{
                    create_language_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {             
                create_language_dialog.html(data);

                $("#id_name").focus();
                
                var create_language_form_validator = $("#create_language_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                            	$("#create_language_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#create_language_form");
                                $("#create_language_form .error_section").html("");
                            },
				            complete: function(jqXHR, textStatus) {
				            	$("#create_language_form input[type=submit]").removeAttr("disabled");
                				create_language_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#create_language_form");
				            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_language_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".create_language_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function(data) {
                                if(data.valid) {
                                    var success_message = "<div class='dialog_content_wrapper'><div class='message_section'><p>The language \"" + data.name + "\" has been created successfully!</p>";
                                    success_message += "<p><a class='select_basic_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Basic)\" to your Languages & Close Dialog</a></p>";
                                    success_message += "<p><a class='select_proficient_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Proficient)\" to your Languages & Close Dialog</a></p>";
                                    success_message += "<p><a class='select_fluent_language_link' href='javascript:void(0)'>Add \"" + data.name + " (Fluent)\" to your Language & Close Dialog</a></p>";
                                    success_message += CLOSE_DIALOG_LINK + "</div>";
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
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_table_form_field_error,
                    rules: {
                        name: {
                            required: true,
                            remote: {
                                url:CHECK_LANGUAGE_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".create_language_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                    }else{
                                        $(".create_language_dialog .error_section").html(ERROR_MESSAGE);
                                    }
                                }
                            }
                        }
                    },
                    messages:{
                        name:{
                            remote: LANGUAGE_ALREADY_EXISTS
                        }
                    }
                });
            }
        });
    });
});