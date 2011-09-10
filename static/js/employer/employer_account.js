$(document).ready( function() {
    function open_account_deletion_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Delete Account",
            dialogClass: "account_deletion_dialog",
            modal:true,
            width:440,
            resizable: false,
            close: function() {
                account_deletion_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('#delete_account_link').click( function () {
        account_deletion_dialog = open_account_deletion_dialog();
        account_deletion_dialog.html(DIALOG_AJAX_LOADER);

        var account_deletion_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: EMPLOYER_ACCOUNT_DELETE_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(account_deletion_dialog_timeout);
                account_deletion_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    account_deletion_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    account_deletion_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                account_deletion_dialog.html(data);
                $("#student_deactivate_account_link").click(function(){
                    $.ajax({
                        type:"POST",
                        dataType: "json",
                        data:{'suggestion':$("#id_suggestion").val()},
                        url: STUDENT_ACCOUNT_DEACTIVATE_URL,
                        beforeSend: function (arr, $form, options) {
                            show_form_submit_loader("#student_account_deactivation_form");
                        },
                        complete : function(jqXHR, textStatus) {
                            hide_form_submit_loader("#student_account_deactivation_form");
                            account_deletion_dialog.dialog('option', 'position', 'center');
                        },
                        success: function (data){
                            if(data.errors){
                                place_table_form_errors("#student_account_deactivation_form", data.errors);  
                            }else{
                                window.location.href = "/?action=account-deactivated";
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            if(jqXHR.status==0){
                                account_deletion_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                            }else{
                                account_deletion_dialog.html(ERROR_MESSAGE_DIALOG);
                            }
                        }
                    });
                });
            }
        });
    });
    
    var create_recruiter_dialog = null;

    function open_create_recruiter_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"New Recruiter Credentials",
            dialogClass: "create_recruiter_dialog",
            modal:true,
            width:475,
            resizable: false,
            close: function() {
                create_recruiter_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

$('.create_recruiter_link').click( function () {
        create_recruiter_dialog = open_create_recruiter_dialog();
        create_recruiter_dialog.html(DIALOG_AJAX_LOADER);
        
        var create_recruiter_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CREATE_RECRUITER_URL,
            complete: function(jqXHR, textStatus) {
                clearTimeout(create_recruiter_dialog_timeout);
                create_recruiter_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    create_recruiter_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    create_recruiter_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                create_recruiter_dialog.html(data);
                var create_recruiter_form_validator = $("#create_recruiter_form").validate({
                    submitHandler: function(form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                $("#create_recruiter_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#create_recruiter_form");
                                $("#create_recruiter_form .error_section").html("");
                            },
                            complete: function(jqXHR, textStatus) {
                                $("#create_recruiter_form input[type=submit]").removeAttr("disabled");
                                create_recruiter_dialog.dialog('option', 'position', 'center');
                                hide_form_submit_loader("#create_recruiter_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".create_recruiter_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".create_recruiter_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function(data) {
                                if (data.errors){
                                    place_table_form_errors("#create_recruiter_form", data.errors);
                                }else{
                                    var success_message = "<div class='message_section'><p>The credentials have been created and can now be used to log in.</p></div>";
                                    success_message += CLOSE_DIALOG_LINK;
                                    create_recruiter_dialog.html(success_message);
                                    $.ajax({
                                        url: EMPLOYER_OTHER_RECRUITERS_URL,
                                        success: function(data){
                                            $("#employer_other_recruiters").replaceWith(data);
                                        },
                                        error: errors_in_message_area_handler
                                    });
                                }
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_table_form_field_error,
                    rules: {
                        first_name:{
                            required: true,
                        },
                        last_name:{
                            required: true,
                        },
                        email: {
                            required: true,
                            email:true,
                            remote: {
                                dataType: 'json',
                                url: CHECK_EMAIL_AVAILABILITY_URL,
                                error: errors_in_message_area_handler
                            }
                        },
                        password1: {
                            required: true,
                            minlength: PASSWORD_MIN_LENGTH
                        },
                        password2: {
                            required: true,
                            equalTo: '#id_password1'
                        }
                    },
                    messages:{
                        email:{
                            remote: EMAIL_ALREADY_REGISTERED
                        },
                        password2:{
                            equalTo: "The passwords you entered don't match."
                        }
                    }
                });
            }
        });
    });
});