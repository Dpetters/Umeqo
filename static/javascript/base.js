/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

/* Multiselect Widget Properties */
var multiselectMinWidth = 318;
var multiselectYesNoSingleSelectWidth = 182;
var multiselectSingleSelectWidth = 202;
var multiselectTwoOptionHeight = 47;
var multiselectMediumHeight = 97;
var multiselectLargeHeight = 146;
var multiselectCheckAllText = "All";
var multiselectUncheckAllText = "None";
var multiselectShowAnimation = "";
var multiselectHideAnimation = "";

var dialog_class = "dialog";
var ajax_loader = "<div class='message_section'></div><div id='dialog_loader'><img src='/static/images/page_elements/loaders/dialog_loader.gif'></div>";
var refresh_page_link = "<div class='message_section'><a class='refresh_page_link' href='javascript:void(0)'>Refresh Page</a></div>";
var close_dialog_link = "<br><div class='message_section'><a class='close_dialog_link' href='javascript:void(0)'>Close Dialog</a></div>";
var generic_error_message = "<div class='message_section'><p>Oops, something went wrong! We'be been notified and will fix it ASAP.</p><br/><p>Meanwhile, you can try again by refreshing the page.</p></div>" + refresh_page_link;
var long_load_message = "<p>This is taking longer than usual. Check your connection and/or <a class='refresh_page_link' href='javascript:void(0)'>refresh</a>.</p>"
var check_connection_message = "<p class='error'>Unable to reach Umeqo. Please check your connection and try again.</p>";

function create_error_dialog() {
    var error_dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title: "Error",
            dialogClass: "error_dialog",
            resizable: false,
            modal: true,
            width: 500,
            close: function() {
                error_dialog.remove();
            }
        });
        error_dialog.dialog('open');
        return error_dialog;
};
function show_error_dialog(message){
	 var error_dialog = create_error_dialog();
     error_dialog.html(message);
};    
function show_loading_failed_message(dialog) {
    $(".dialog .message_section").html(long_load_message);
};
function show_form_submit_loader(container) {
    container = typeof(container) != 'undefined' ? container : "";
    $(container + " #ajax_form_submit_loader").css("display", "");
};
function hide_form_submit_loader() {
    container = typeof(container) != 'undefined' ? container : "";
    $(container + " #ajax_form_submit_loader").css("display", "none");
};
// Validation Highlighting, unhighlighting and positioning of errors
function highlight(element, errorClass) {
    if ($(element).next(":button.ui-multiselect") != []) {
        $(element).next().css('border', '1px solid #FF603D');
    }
    $(element).filter("input[type=password]").css('border', '1px solid #FF603D');
    $(element).filter("input[type=text]").css('border', '1px solid #FF603D');
    $(element).filter("select").css('border', '1px solid #FF603D');
};
function unhighlight(element, errorClass) {
    if ($(element).next(":button.ui-multiselect")) {
        $(element).next().css('border', '1px solid #AAA');
    }
    $(element).filter("input[type=password]").css('border', '1px solid #AAA');
    $(element).filter("input[type=text]").css('border', '1px solid #AAA');
    $(element).filter("select").css('border', '1px solid #AAA');
};
function place_errors(error, element) {
    $(error).appendTo(element.parent().prev());
    if ($(element).position().left == 0) {
        if ($(element).next(":button.ui-multiselect").length!=0) {
            var offset = element.next().position().left-element.parent().position().left;
        }
    } else {
        var offset = element.position().left-element.parent().position().left;
    }
    $(error).css({
        "padding-left": offset,
        "float": "left",
        "position": "absolute",
        "bottom": 0
    });
};
function place_errors_table(error,element) {
    if (element.prev().get(0).tagName=='DIV') {
        $(error).appendTo(element.prev());
    } else if (element.prev().prev().html()=="" || !element.prev().prev().children(":eq(0)").is(":visible")){
        $(error).appendTo(element.prev().prev());
    }
    if ($(element).position().left == 0) {
        if ($(element).next(":button.ui-multiselect").length!=0) {
            var offset = element.next().position().left-element.parent().position().left;
        }
    } else if (element.prev().prev().get(0) && element.prev().prev().get(0).tagName!='DIV'){
        console.log(element.prev().prev());
        var offset = element.position().left-element.parent().position().left;
    }
    $(error).css({
        "padding-left": offset,
        "float": "left",
        "position": "absolute",
        "bottom": 0
    });
}
// Multiselect Warning Function
function show_multiselect_warning(e, max) {
    var element = $("#" + e)
    var error = $("<label class='warning' for'" + e + "'>You can check at most " + max + " checkboxes.</label>");
    $(error).appendTo(element.parent().prev());
    $(error).css("padding-left", $(element).prev().outerWidth()+3).css("float", "left").css('position', 'absolute').css('bottom','0');
};
// Pick out url GET parameters by name
function get_parameter_by_name(name) {
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if( results == null )
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
}
// Helper method for accessing cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Get max of array
Array.max = function (array) {
    return Math.max.apply(Math, array);
};
    
$(document).ready( function () {
    
    /* Contact Dialog */
    var create_contact_dialog = function () {
        var $contact_us_dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title: "Contact Us",
            dialogClass: "contact_us_dialog",
            resizable: false,
            modal: true,
            width: 650,
            close: function() {
                $contact_us_dialog.remove();
            }
        });
        $contact_us_dialog.dialog('open');
        return $contact_us_dialog;
    };
    $('.open_contact_us_dialog_link').live('click', function () {

        var $contact_us_dialog = create_contact_dialog();
        $contact_us_dialog.html(ajax_loader);

        var contact_us_dialog_timeout = setTimeout(show_loading_failed_message, 10000);
        $.ajax({
            dataType: "html",
            url: '/contact-us-dialog/',
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(contact_us_dialog_timeout);
                show_error_dialog(generic_error_message);
            },
            success: function (data) {
                clearTimeout(contact_us_dialog_timeout);

                $contact_us_dialog.html(data);
                $("#id_name").focus();

                contact_form_validator = $("#contact_form").validate({
                    submitHandler: function (form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#contact_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"' + textStatus + '"</strong></div>';
                                $contact_us_dialog.html(error_message_template + error_message_details + close_dialog_link);
                            },
                            success: function (data) {

                                hide_form_submit_loader("#contact_form");

                                switch(data.valid) {
                                    case true:
                                        var success_message = "<br><div class='message_section'><p>We have received your message. Thanks for contacting us!</p></div>";
                                        success_message += close_dialog_link;
                                        $contact_us_dialog.html(success_message);
                                        $contact_us_dialog.dialog('option', 'position', 'center');
                                        break;
                                    case false:
                                        $("#dialog_form_error_section").html("<p class='error'>Our system thinks your message is spam. If you think this is a mistake, email us instead at support@umeqo.com.</p>");
                                        break;
                                    default:
                                        var error_message_details = '<div class="message_section"><strong><br />Error Details</strong><br />"Response status isn\'t valid."</strong></div>';
                                        error_message_details += close_dialog_link;
                                        $contact_us_dialog.html(error_message_template + error_message_details);
                                        break;
                                }
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors,
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
                    }
                });
            }
        });
    });
    
    // Make sure dialogs are always position in the center
    $(window).resize( function() {
        $(".dialog").dialog('option', 'position', 'center');
    });
    $(window).scroll( function() {
        $(".dialog").dialog('option', 'position', 'center');
    });
    
    $(".close_dialog_link").live('click', function() {
        $(".dialog").remove();
    });
    
    $(".refresh_page_link").live('click', function() {
        window.location.reload();
    });

    /* JQuery Validator Additions */
    jQuery.validator.addMethod("notEqualToString", function(value, element, param) {
        return this.optional(element) || value != param;
    }, "Please specify a different (non-default) value");
    jQuery.validator.addMethod("notEqualTo", function(value, element, param) {
        return this.optional(element) || value != $(param).val();
    }, "Please specify a different (non-default) value");
    jQuery.validator.addMethod("notAllZeroes", function(value, element) {
        if($("#id_days").val() == 0 && $("#id_hours").val() == 0 && $("#id_minutes").val() == 0) {
            $("#id_days, #id_hours, #id_minutes").attr('style', "border: 1px solid #FF603D !important");
            return false;
        } else {
            $("#id_days, #id_hours, #id_minutes").attr('style', "border: 1px solid #808080");
            return true;
        }
    }, "Please specify a valid duration");
});