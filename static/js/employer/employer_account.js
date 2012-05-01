var create_recruiter_dialog = null;

function open_account_deletion_dialog() {
    var $dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"Delete Account",
        dialogClass: "account_deletion_dialog",
        modal:true,
        width:410,
        resizable: false,
        close: function() {
            account_deletion_dialog.remove();
        }
    });
    $dialog.dialog('open');
    return $dialog;
};

function delete_account_link_click_handler() {
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
            $("#delete_account_confirmation_link").click(function(){
                $.ajax({
                    type:"POST",
                    dataType: "json",
                    url: EMPLOYER_ACCOUNT_DELETE_URL,
                    success: function (data){
                        window.location.href = "/?action=account-deactivated";
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
}

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
}

function create_recruiter_credentials_link_click_handler() {
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
                                $("#delete_account").show();
                                $("#create_credentials").hide() 
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
                        equalTo: PASSWORD_DONT_MATCH
                    }
                }
            });
        }
    });
}

$(document).ready( function() {
    if (ONLY_RECRUITER){
        $("#delete_account").hide();
        $("#create_credentials").show();
    }else{
        $("#delete_account").show();
        $("#create_credentials").hide();
    }

    if (get_parameter_by_name("tab")=="subscription"){
        $("#preferences_form_tabs").tabs("select", 2);
    }
    
    if (SUBSA && get_parameter_by_name("action")=="new_recruiter_credentials"){
        create_recruiter_credentials_link_click_handler();
    } else if (!ONLY_RECRUITER && get_parameter_by_name("action")=="delete_account"){
        delete_account_link_click_handler();
    }

    $('#delete_account_link').click( delete_account_link_click_handler);
    $('.create_recruiter_link').click( create_recruiter_credentials_link_click_handler);

});