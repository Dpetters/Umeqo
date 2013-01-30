$(document).ready( function() {
    var school_new_dialog = null;

    function open_school_new_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New School",
            dialogClass: "school_new_dialog",
            modal:true,
            width:430,
            resizable: false,
            close: function() {
                school_new_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

$('.open_school_new_dialog_link').click( function () {
        school_new_dialog = open_school_new_dialog();
        school_new_dialog.html(DIALOG_AJAX_LOADER);
        
        var school_new_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: SCHOOL_NEW_DIALOG_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(school_new_dialog_timeout);
                school_new_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    school_new_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    school_new_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                school_new_dialog.html(data);
                
                $("#id_name").focus();
                
                var school_new_form_validator = $("#school_new_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                $("#school_new_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#school_new_form");
                                $("#school_new_form .error_section").html("");
                            },
                            complete: function(jqXHR, textStatus) {
                                $("#school_new_form input[type=submit]").removeAttr("disabled");
                                school_new_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#school_new_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".school_new_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".school_new_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function(data) {
                                if (data.errors) {
                                    place_table_form_errors("#school_new_form", data.errors);
                                } else {
                                    $("#id_school").append('<option name="' + data.name + '" value="' + data.id + '">' + data.name + '</option>').attr('selected', true);
 
                                    var success_message = "<div class='dialog_content_wrapper'><div class='message_section'><p>The listing for \"" + data.name + "\" has been created successfully!</p>";
                                    success_message += "<p><a id='select_new_school_link' href='#'>Set it as your school  & close dialog</a></p>";
                                    success_message += CLOSE_DIALOG_LINK + "</div>";
                                    school_new_dialog.html(success_message);

                                    // Marks the new campus org as selected on the actual select field, updates the widget, and then closes the dialog
                                    $("#select_new_school_link").click(function() {
                                        $("#id_school option[name='" + data.name +"']").attr('selected', true);
                                        school_new_dialog.dialog('destroy');
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
                                url: CHECK_SCHOOL_UNIQUENESS_URL,
                                error: function(jqXHR, textStatus, errorThrown) {
                                    if(jqXHR.status==0){
                                        $(".school_new_dialog .error_section").html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                    }else{
                                        school_new_dialog.html(ERROR_MESSAGE_DIALOG);
                                    }
                                    school_new_dialog.dialog('option', 'position', 'center');
                                }
                            }
                        },
                        url: {
                            complete_url: true
                        }
                    },
                    messages:{
                        name:{
                            remote: SCHOOL_ALREADY_EXISTS
                        }
                    }
                });
            }
        });
    });
});
