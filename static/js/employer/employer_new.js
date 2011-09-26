$(document).ready( function() {
    var create_employer_dialog = null;

    function open_create_employer_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Employer",
            dialogClass: "create_employer_dialog",
            modal:true,
            width:430,
            resizable: false,
            close: function() {
                console.log("removing");
                create_employer_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    $('.create_employer_link').click( function (e) {
        create_employer_dialog = open_create_employer_dialog();
        create_employer_dialog.html(DIALOG_AJAX_LOADER);
            
        var create_employer_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: EMPLOYER_NEW_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_employer_dialog_timeout);
                create_employer_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    create_employer_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    create_employer_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                create_employer_dialog.html(data);
                
                $("#id_industries").multiselect({
                    noneSelectedText: 'select industries',
                    classes: 'industries_multiselect',
                    uncheckAllText: multiselectUncheckAllText,
                    minWidth:250,
                    beforeclose: function() {
                        $(".warning").remove();
                    },
                    click: function(e) {
                        $(".warning").remove();
                        if( $(this).multiselect("widget").find("input:checked").length > MAX_INDUSTRIES ) {
                            place_multiselect_warning_table($("#id_industries"), MAX_INDUSTRIES_EXCEEDED);
                            return false;
                        }
                    }
                }).multiselectfilter();
                
                $("#id_name").focus();
                
                var create_employer_form_validator = $("#create_employer_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                $("#create_employer_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#create_employer_form");
                                $("#create_employer_form .error_section").html("");
                            },
                            complete: function(jqXHR, textStatus) {
                                $("#create_employer_form input[type=submit]").removeAttr("disabled");
                                create_employer_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#create_employer_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_employer_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".create_employer_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function(data) {
                                if (data.errors) {
                                    place_table_form_errors("#create_employer_form", data.errors);
                                }else{
                                    var success_message = "<div class='dialog_content_wrapper'><div class='message_section'><p>The employer \"" + data.name + "\" has been created successfully!</p>";
                                    if (typeof(EVENT)!="undefined"){
                                        success_message += "<p><a class='select_new_employer_link' href='#'>Mark " + data.name + " as attending  & Close Dialog</a></p>";
                                    }else{
                                        if( $("#id_previous_employers").multiselect("widget").find("input:checked").length <= PREVIOUS_EMPLOYERS_MAX-1 ) {
                                            success_message += "<p><a class='select_new_employer_link' href='#'>Add it to your previous employers & Close Dialog</a></p>";
                                        }
                                    }
                                    success_message += CLOSE_DIALOG_LINK + "</div>";
                                    create_employer_dialog.html(success_message);
    
                                    // Add the new campus organization to the select and update the widget to include it
                                    if (typeof(EVENT)!="undefined"){
                                        selector = "#id_attending_employers"
                                    } else {
                                        selector = "#id_previous_employers"
                                    }
                                    $(selector).append('<option name="' + data.name + '" value="' + data.id + '">' + data.name + '</option>');
                                    $(selector).multiselect("refresh");
                                    $(selector).multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                    // Marks the new employer as selected on the actual select field, updates the widget, and then closes the dialog
                                    $(".select_new_employer_link").click(function(e) {
                                        $(selector).find('option[name="' + data.name + '"]').attr('selected', true);
                                        $(selector).multiselect("refresh");
                                        $(selector).multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                        create_employer_dialog.remove();
                                        if (typeof(EVENT)!="undefined"){
                                            display_attending_employer(data.name);
                                        }
                                        e.preventDefault();
                                    });
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
                                url: CHECK_EMPLOYER_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".create_employer_dialog .error_section").html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                        create_employer_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                    create_employer_dialog.dialog('option', 'position', 'center');
                                }
                            }
                        },
                        industries: {
                            required: true
                        },
                    },
                    messages:{
                        name:{
                            remote: EMPLOYER_ALREADY_EXISTS
                        }
                    }
                });
            }
        });
        e.preventDefault();
    });
});