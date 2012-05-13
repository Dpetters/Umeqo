$(document).ready( function() {
    var create_campus_org_dialog = null;

    function open_create_campus_org_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Campus Organization",
            dialogClass: "create_campus_org_dialog",
            modal:true,
            width:480,
            resizable: false,
            close: function() {
                create_campus_org_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

$('#create_campus_organization_link').click( function () {
        create_campus_org_dialog = open_create_campus_org_dialog();
        create_campus_org_dialog.html(DIALOG_AJAX_LOADER);
        
        var create_campus_org_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CREATE_CAMPUS_ORGANIZATION_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_campus_org_dialog_timeout);
                create_campus_org_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    create_campus_org_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    create_campus_org_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                create_campus_org_dialog.html(data);
                
                $("#id_name").focus();
                
                var create_campus_org_form_validator = $("#create_campus_org_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                $("#create_campus_org_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#create_campus_org_form");
                                $("#create_campus_org_form .error_section").html("");
                            },
                            complete: function(jqXHR, textStatus) {
                                $("#create_campus_org_form input[type=submit]").removeAttr("disabled");
                                create_campus_org_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#create_campus_org_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_campus_org_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".create_campus_org_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function(data) {
                                if (data.errors) {
                                    place_table_form_errors("#create_campus_org_form", data.errors);
                                } else {
                                    var success_message = "<div class='dialog_content_wrapper'><div class='message_section'><p>The listing for \"" + data.name + "\" has been created successfully!</p>";
                                    if( $("#id_campus_involvement").multiselect("widget").find("input:checked").length <= CAMPUS_INVOLVEMENT_MAX-1 ) {
                                        success_message += "<p><a id='select_new_campus_org_profile_link' href='#'>Add it to your Campus Involvement  & Close Dialog</a></p>";
                                    }
                                    success_message += CLOSE_DIALOG_LINK + "</div>";
                                    create_campus_org_dialog.html(success_message);

                                    // Add the new campus organization to the select and update the widget to include it
                                    $("optgroup[label='" + data.type + "']").append('<option name="' + data.name + '" value="' + data.id + '">' + data.name + '</option>');
                                    $("#id_campus_involvement").multiselect("refresh");
                                    $("#id_campus_involvement").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                    if( $("#id_campus_involvement").multiselect("widget").find("input:checked").length <= CAMPUS_INVOLVEMENT_MAX-1 ) {
                                        // Marks the new campus org as selected on the actual select field, updates the widget, and then closes the dialog
                                        $("#select_new_campus_org_profile_link").click(function() {
                                            $("#id_campus_involvement").find('option[name="' + data.name + '"]').attr('selected', true);
                                            $("#id_campus_involvement").multiselect("refresh");
                                            $("#id_campus_involvement").multiselect("widget").find(".ui-multiselect-optgroup-label").show();
                                            create_campus_org_dialog.dialog('destroy');
                                        });
                                    }
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
                                url: CHECK_CAMPUS_ORG_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".create_campus_org_dialog .error_section").html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                        create_campus_org_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                    create_campus_org_dialog.dialog('option', 'position', 'center');
                                }
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
                            remote: CAMPUS_ORG_ALREADY_EXISTS
                        }
                    }
                });
            }
        });
    });
});