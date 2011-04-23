/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {

    /* The main blocks that we use need to have their line-heights set
     * to their heights so that icons & text get position in the center
     * vertically. To do so, I first fix the height manually, and then 
     * allow it to be modified as the icons are loaded.
     */
     /*
    fix_header_line_height = function() {
        $(".main_block_header, .side_block_header, .main_area_header").each( function(inx, element) {
            $(element).css("line-height", $(element).css("height"));
        });
    };
    fix_header_line_height();
    $(".main_block_header_icon, .side_block_header_icon").load(function(){
        var header = $(this).parents(".main_block_header, .side_block_header, .main_area_header");
        $(header).css("line-height", $(header).css("height"));
    });
    */
    
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
            success: function (data) {
                clearTimeout(contact_us_dialog_timeout);

                $contact_us_dialog.html(data);
                $("#id_name").focus();
                $contact_us_dialog.dialog('option', 'position', 'center');

                format_required_labels("#contact_form");
                align_form("#contact_form");

                $("label[for=id_body]").css('padding-left', '0px');

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
                                        $("#dialog_form_error_section").html("<p class='error'>Our system thinks your message is spam. If you think this is a mistake, email us instead at support@sbconnect.com.</p>");
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
    /* Event Binding */
    
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
    
    /* Function Definitions */
    
    // Aligns the inputs of a form
    /*align_form = function(container, shift) {
        container = typeof(container) != 'undefined' ? container : "";
        shift = typeof(shift) != 'undefined' ? shift : 0;

        var widths = [];
        $(container + ' label').each( function(idx, label) {
            widths.push(label.offsetWidth);
        });
        $(container + ' label').each( function(idx, label) {
            var diff = Array.max(widths) - this.offsetWidth;
            label.style.paddingLeft = diff + shift + "px";
        });
    };*/
    // Form Required Label Formatting
    /*format_required_labels = function(container) {
        container = typeof(container) != 'undefined' ? container : "";
        $(container + " .required").css('font-weight', 'bold').append("<span class='error'>*</span>");
    };*/
    show_loading_failed_message = function(dialog) {
        $(".dialog .message_section").html("This is taking longer than usual. Check your connection and/or <a class='refresh_page_link' href='javascript:void(0)'>refresh</a>.");
    };
    show_form_submit_loader = function (container) {
        container = typeof(container) != 'undefined' ? container : "";
        $(container + " #ajax_form_submit_loader").css("display", "");
    };
    hide_form_submit_loader = function () {
        container = typeof(container) != 'undefined' ? container : "";
        $(container + " #ajax_form_submit_loader").css("display", "none");
    };
    // Validation Highlighting, unhighlighting and positioning of errors
    highlight = function(element, errorClass) {
        if ($(element).next(":button.ui-multiselect") != []) {
            $(element).next().css('border', '1px solid #FF603D');
        }
        $(element).filter("input[type=password]").css('border', '1px solid #FF603D');
        $(element).filter("input[type=text]").css('border', '1px solid #FF603D');
        $(element).filter("select").css('border', '1px solid #FF603D');
    };
    unhighlight = function (element, errorClass) {
        if ($(element).next(":button.ui-multiselect")) {
            $(element).next().css('border', '1px solid #AAA');
        }
        $(element).filter("input[type=password]").css('border', '1px solid #AAA');
        $(element).filter("input[type=text]").css('border', '1px solid #AAA');
        $(element).filter("select").css('border', '1px solid #AAA');
    };
    place_errors = function(error, element) {
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
    place_errors_table = function(error,element) {
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
    show_multiselect_warning = function(e, max) {
        var element = $("#" + e)
        var error = $("<label class='warning' for'" + e + "'>You can check at most " + max + " checkboxes.</label>");
        $(error).appendTo(element.parent().prev());
        $(error).css("padding-left", $(element).prev().outerWidth()+3).css("float", "left").css('position', 'absolute').css('bottom','0');
    };
    // Default text for input fields
    /*
    add_default_text_to_input = function(input, old_query, default_text) {
        var active_color = '#000';
        var inactive_color = '#aaa';
        var default_value = default_text;
        if (old_query)
            $(input).css("color", active_color).val(old_query);
        else
            $(input).css("color", inactive_color).val(default_value);

        $(input).live('focus', function() {
            if (this.value == default_value) {
                this.value = "";
                this.style.color = active_color;
            }
        }).live('blur', function() {
            if (this.value == "") {
                this.value = default_value;
                this.style.color = inactive_color;
            }
        });
    };
    */
    // Pick out url GET parameters by name
    get_parameter_by_name = function(name) {
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
    getCookie = function(name) {
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

    /* Objects */
    dialog_class = "dialog";
    ajax_loader = "<div class='message_section'></div><div id='dialog_loader'><img src='/static/images/page_elements/loaders/dialog_loader.gif'></div>";
    refresh_page_link = "<div class='message_section'><a class='refresh_page_link' href='javascript:void(0)'>Refresh Page</a></div>";
    close_dialog_link = "<br><div class='message_section'><a class='close_dialog_link' href='javascript:void(0)'>Close Dialog</a></div>";
    status_500_message = "<div class='message_section'><p>Oops, something went wrong! We'be been notified and will fix it ASAP.</p><br/><p>Meanwhile, you can try again by refreshing the page.</p></div>" + refresh_page_link;
    check_connection_message = "<p class='error'>Unable to reach Umeqo. Please check your connection and try again.</p>";
    

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
    
    $('.fade_input_label input').focus(function(){
        $(this).prev().animate({'opacity':0},200);
    });
    $('.fade_input_label input').each(function(){
        if ($(this).val()!="") {
            $(this).prev().css('opacity',0);
        }
    });
    $('.fade_input_label input').blur(function(){
       if ($(this).val()=="") {
           $(this).prev().animate({'opacity':1},200);
       } 
    });
    
});