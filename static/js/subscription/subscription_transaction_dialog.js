$(document).ready( function() {
    function open_subscription_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            dialogClass: "subscription_dialog",
            modal:true,
            width:535,
            resizable: false,
            close: function() {
                subscription_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    $('.open_subscription_dialog_link.upgrade, .open_subscription_dialog_link.downgrade, .open_subscription_dialog_link.subscribe, .open_subscription_dialog_link.cancel').click( function () {
        subscription_dialog = open_subscription_dialog();
        subscription_dialog.dialog("option", "title", $(this).attr("data-title"));
        subscription_dialog.html(DIALOG_AJAX_LOADER);

        var subscription_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        var action = $(this).attr("data-action");
        var type = $(this).attr("data-type");
        
        $.ajax({
            type:'GET',
            dataType: "html",
            url: SUBSCRIPTION_TRANSACTION_URL,
            data: {'type':type, 'action':action},
            complete: function(jqXHR, textStatus) {
                clearTimeout(subscription_dialog_timeout);
                subscription_dialog.dialog('option', 'position', 'center');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(jqXHR.status==0){
                    subscription_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                }else{
                    subscription_dialog.html(ERROR_MESSAGE_DIALOG);
                }
            },
            success: function (data) {
                subscription_dialog.html(data);
                subscription_form_validator = $("#subscription_form").validate({
                    submitHandler: function (form) {
                        console.log(type);
                        console.log(action);
                        $(form).ajaxSubmit({
                            url: SUBSCRIPTION_TRANSACTION_URL,
                            data: {'type':type, 'action':action},
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                $("#subscription_form input[type=submit]").attr("disabled", "disabled");
                                show_form_submit_loader("#subscription_form");
                                $("#subscription_form .errorspace, #contact_us_form .error_section").html("");
                            },
                            complete : function(jqXHR, textStatus) {
                                subscription_dialog.dialog('option', 'position', 'center');
                                $("#subscription_form input[type=submit]").removeAttr("disabled");
                                hide_form_submit_loader("#subscription_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0){
                                    $(".subscription_dialog .error_section").html(CHECK_CONNECTION_MESSAGE);
                                }else{
                                    $(".subscription_dialog .error_section").html(ERROR_MESSAGE);
                                }
                            },
                            success: function (data) {
                                if(data.valid) {
                                    var success_message = "<div class='message_section'><p>" + data.success_message + "</p></div>";
                                    success_message += CLOSE_DIALOG_LINK;
                                    subscription_dialog.html(success_message);
                                } else {
                                    place_table_form_errors("#subscription_form", data.errors);
                                }
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_table_form_field_error,
                    rules: {
                        name: {
                            required: true
                        },
                        email: {
                            required: true,
                            email: true
                        },
                        body: {
                            required: true
                        }
                    },
                    messages: {
                        email: {
                            email: "Please enter a valid email."
                        }
                    }
                });
            }
        });
    });
});