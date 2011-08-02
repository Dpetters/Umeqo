var PASSWORD_MIN_LENGTH = 5;
var LOAD_WAIT_TIME = 8000;

/* Multiselect Widget Properties */
var multiselectMinWidth = 318;
var multiselectYesNoSingleSelectWidth = 181;
var multiselectSingleSelectWidth = 202;
var multiselectCheckAllText = "All";
var multiselectUncheckAllText = "None";

function create_error_dialog() {
    var error_dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title: "Server Error",
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
     error_dialog = create_error_dialog();
     error_dialog.html(message);
};    

function show_long_load_message_in_dialog(dialog) {
    $("#dialog_loader p").html(single_line_long_load_message);
};

function show_form_submit_loader(container) {
    var container = typeof(container) != 'undefined' ? container : "";
    if (container)
        $(container + " #ajax_form_submit_loader").show();
};
function hide_form_submit_loader(container) {
    var container = typeof(container) != 'undefined' ? container : "";
    if (container)
        $(container + " #ajax_form_submit_loader").hide();
};
function place_TINY_AJAX_LOADER(container) {
    container = typeof(container) != 'undefined' ? container : "";
    if (container)
        $(container).html(TINY_AJAX_LOADER);
};
// Validation Highlighting, unhighlighting and positioning of errors
function highlight(element, errorClass) {
    if ($(element).next(":button.ui-multiselect").length != 0) {
        $(element).next().css('border', '1px solid #FF603D');
    }
    $(element).filter("input[type=password]").css('border', '1px solid #FF603D');
    $(element).filter("input[type=text]").css('border', '1px solid #FF603D');
    $(element).filter("select").css('border', '1px solid #FF603D');
};
function unhighlight(element, errorClass) {
    $(element).prev().children().hide();
    if ($(element).next(":button.ui-multiselect").length != 0) {
        $(element).next().css('border', '1px solid #AAA');
    }
    $(element).filter("input[type=password]").css('border', '1px solid #AAA');
    $(element).filter("input[type=text]").css('border', '1px solid #AAA');
    $(element).filter("select").css('border', '1px solid #AAA');
};

function place_table_form_errors(form, errors){
    for (error in errors){
        if (error == "non_field_error"){
            $(form + " .error_section").html(errors[error]);
        }
        else{
            place_errors_table($("<label class='error' for='" + error + "'>" + errors[error] + "</label>"), $("#"+error));
        }
    };
};
/*
 * Places field errors which got returned from an ajax submit in a table forms
 * Currently we show on field error at a time
 */
function place_errors_ajax_table(errors, element){
    var error = "<label class='error' for='" + element.text() + "'>" + errors[0] + "</label>";
    place_errors_table($(error), element);
};

function place_errors_table($error, $element) {
    if ($element.prev().get(0).tagName=='DIV') {
        $element.prev().html($error);
    } else if ($element.prev().prev().html()=="" || !$element.prev().prev().children(":eq(0)").is(":visible")){
        $element.prev().prev().html($error);
    }
    if ($element.position().left == 0) {
        if ($element.next(":button.ui-multiselect").length!=0) {
            var offset = $element.next().position().left-$element.parent().position().left;
        }
    } else if ($element.prev().prev().get(0) && $element.prev().prev().get(0).tagName!='DIV'){
        var offset = $element.position().left - $element.parent().position().left;
    }
    $error.css({
        "padding-left": offset,
        "float": "left",
        "position": "absolute",
        "bottom": 0
    });
}
// Shows max number that one can select on that multiselect
function place_multiselect_warning_table(element, max) {
    var warning = $("<label class='warning' for'" + element.attr("id") + "'>You can check at most " + max + " checkboxes.</label>");
    place_errors_table($(warning), element)
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

// number formatting function
// copyright Stephen Chapman 24th March 2006, 10th February 2007
// permission to use this function is granted provided
// that this copyright notice is retained intact
function formatNumber(num,dec,thou,pnt,curr1,curr2,n1,n2)
{
  var x = Math.round(num * Math.pow(10,dec));
  if (x >= 0) n1=n2=''; 

  var y = (''+Math.abs(x)).split('');
  var z = y.length - dec; 

  if (z<0) z--; 

  for(var i = z; i < 0; i++)
    y.unshift('0'); 

  y.splice(z, 0, pnt);
  if(y[0] == pnt) y.unshift('0'); 

  while (z > 3)
  {
    z-=3;
    y.splice(z,0,thou);
  } 

  var r = curr1+n1+y.join('')+n2+curr2;
  return r;
}

// Get max of array
Array.max = function (array) {
    return Math.max.apply(Math, array);
};
    
$(document).ready( function () {
    
    /* Contact Dialog */
    var open_contact_us_dialog = function () {
        var contact_us_dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title: "Contact Us",
            dialogClass: "contact_us_dialog",
            resizable: false,
            modal: true,
            width: 600,
            close: function() {
                contact_us_dialog.remove();
            }
        });
        contact_us_dialog.dialog('open');
        return contact_us_dialog;
    };
    $('.open_contact_us_dialog_link').live('click', function () {

        contact_us_dialog = open_contact_us_dialog();
        contact_us_dialog.html(DIALOG_AJAX_LOADER);

        var contact_us_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
        $.ajax({
            dataType: "html",
            url: CONTACT_US_URL,
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(contact_us_dialog_timeout);
                if(jqXHR.status==0){
                    contact_us_dialog.html(dialog_check_connection_message);
                }else{
                    contact_us_dialog.html(dialog_error_message);
                }
            },
            success: function (data) {
                clearTimeout(contact_us_dialog_timeout);
                contact_us_dialog.html(data);
                contact_us_dialog.dialog('option', 'position', 'center');
                
                contact_us_form_validator = $("#contact_us_form").validate({
                    submitHandler: function (form) {
                        $(form).ajaxSubmit({
                            dataType: 'json',
                            beforeSubmit: function (arr, $form, options) {
                                show_form_submit_loader("#contact_us_form");
                            },
                            complete : function(jqXHR, textStatus) {
                                hide_form_submit_loader("#contact_us_form");
                            },
                            error: function(jqXHR, textStatus, errorThrown){
                                if(jqXHR.status==0 && errorThrown != "abort"){
                                    $(".contact_us_dialog .error_section").html(form_check_connection_message);
                                }else{
                                    contact_us_dialog.html(dialog_error_message);
                                }
                                contact_us_dialog.dialog('option', 'position', 'center');
                            },
                            success: function (data) {
                                if(data.valid) {
                                    var success_message = "<div class='message_section'><p>" + THANK_YOU_FOR_CONTACTING_US_MESSAGE + "</p></div>";
                                    success_message += CLOSE_DIALOG_LINK;
                                    contact_us_dialog.html(success_message);
                                } else {
                                    place_table_form_errors("#contact_us_form", data.errors);
                                }
                                contact_us_dialog.dialog('option', 'position', 'center');
                            }
                        });
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors_table,
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
    
	$(window).scroll(function() {
	    if(this.scrollTO) clearTimeout(this.scrollTO);
	    this.scrollTO = setTimeout(function() {
	        $(this).trigger('scrollEnd');
	    }, 100);
	});
	
	$(window).resize(function() {
	    if(this.resizeTO) clearTimeout(this.resizeTO);
	    this.resizeTO = setTimeout(function() {
	        $(this).trigger('resizeEnd');
	    }, 100);
	});
	    
	    
    // Make sure dialogs are always position in the center
    $(window).bind('resizeEnd',  function() {
        $(".dialog").dialog('option', 'position', 'center');
    });
    $(window).bind('scrollEnd', function() {
        $(".dialog").dialog('option', 'position', 'center');
    });
    
    $(".close_dialog_link").live('click', function() {
        $(".dialog").remove();
    });
    
    $(".refresh_page_link").live('click', function() {
        window.location.reload();
    });

    jQuery.validator.addMethod("complete_url", function(val, elem) {
        // if no url, don't do anything
        if (val.length == 0) { return true; }
     
        // if user has not entered http:// https:// or ftp:// assume they mean http://
        if(!/^(https?|ftp):\/\//i.test(val)) {
            val = 'http://'+val; // set both the value
            $(elem).val(val); // also update the form element
        }
        // now check if valid url
        // http://docs.jquery.com/Plugins/Validation/Methods/url
        // contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
        return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(val);
    })

    /* JQuery Validator Additions */
    jQuery.validator.addMethod("multiemail", function(value, element, param) {
         if (this.optional(element)) // return true on optional element 
             return true; 
        var emails = value.split( new RegExp( "\\s*[;, \\n]\\s*", "gi" ) );
        valid = true; 
         for(var i in emails) {
            value = emails[i];
            if(value)
                valid=valid && jQuery.validator.methods.email.call(this, value, element);
        } 
        return valid;
    }, "One of the emails you entered is invalid.");
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

    // NOTIFICATIONS.
    $('#notifications_count').click(function() {
        if (!$('#notifications_pane').is(':visible')) {
            $.get(NOTIFICATIONS_URL, function(data) {
                $('#notifications_pane').html(data);
            });
            $('#notifications_number').addClass('invisible');
            $('#notifications_count').addClass('active');
        } else {
            $('#notifications_count').removeClass('active');
        }
        $('#notifications_pane').toggle();
    });

    $(document).keydown(function(e) {
        if (e.which == 27) {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('active');
        }
    });
    $(document).click(function(e) {
        if ($(e.target).parents('#notifications_pane').length == 0 &&
            e.target.id != 'notifications_count') {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('active');
        }
    });

});

/* THIS ADDS CSRF PROTECTION TO AJAX CALLS */
$(document).ajaxSend(function(event, xhr, settings) {
function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
