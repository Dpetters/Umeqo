/* Multiselect Widget Properties */
var multiselectMinWidth = 318;
var multiselectYesNoSingleSelectWidth = 181;
var multiselectSingleSelectWidth = 202;
var multiselectCheckAllText = "All";
var multiselectUncheckAllText = "None";

function update_ckeditors(){
    console.log("hi");
    for (instance in CKEDITOR.instances){
        CKEDITOR.instances[instance].updateElement();
    }        
}

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
function errors_in_message_area_handler(jqXHR, textStatus, errorThrown) {
    if (errorThrown != "abort"){
        if(jqXHR.status==0){
            $("#message_area").html("<p>" + CHECK_CONNECTION_MESSAGE + "</p>");
        }else{
            $("#message_area").html("<p>" + ERROR_MESSAGE + "</p>");
        }
    }
};
function place_table_form_errors(form, errors){
    for (field in errors){
        if (field == "__all__"){
            $(form + " .error_section").html(errors[field][0]);
        }
        else{
            place_table_form_field_error($("<label class='error' for='" + field + "'>" + errors[field] + "</label>"), $("#id_"+field));
        }
    };
};
/* The reason the parameters here are jquery objects is because that's the form in which
 * the jquery form validation plugin passes them. Therefore, even though it's ugly, you
 * should not change the parameters to be non-jquery objects.
 */
function place_table_form_field_error($error, $element) {
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
    $error.css("padding-left", offset);
};
// Shows max number that one can select on that multiselect
function place_multiselect_warning_table(element, message) {
    var warning = $("<label class='warning' for'" + element.attr("id") + "'> " + message + "</label>");
    place_table_form_field_error($(warning), element);
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
function supports_geolocation() {
  return !!navigator.geolocation;
}
Array.max = function (array) {
    return Math.max.apply(Math, array);
};
   
$(document).ready( function () {    
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
    $("a, .button, .dark_button, .dropdown_menu_button, \
    .dropdown_menu_button ul li, .menu_button, .current_page_link, \
    .page_link, .disabled_page_link, #logo_beta, #notifications_count").live({
        mouseleave:
            function(){
                $(this).removeClass('um-active');
            }
    });
    $(".button, .dark_button, .ui-multiselect-menu .ui-multiselect-none, \
    .ui-multiselect-menu .ui-multiselect-all").live("focus", function(){
        $(this).addClass("um-focus");
    });
    $(".button, .dark_button, .ui-multiselect-menu .ui-multiselect-none, \
    .ui-multiselect-menu .ui-multiselect-all").live("focusout", function(){
        $(this).removeClass("um-focus");
    });
    $('.button, .menu_button, .dark_button, #notifications_count').live('mousedown', function() {
        $(this).addClass('um-active');
    });
    $('.button, .menu_button, .dark_button, #notifications_count').live('mouseup', function(){
        if ($(this).hasClass('um-active'))
            $(this).removeClass('um-active');
    });
    $('.dropdown_menu_button').live('click', function() {
        if ($(this).hasClass('um-pressed'))
            $(this).removeClass('um-pressed');
        else
            $(this).addClass('um-pressed');
    });
    $('body').live('click', function(event) {
        if (!$(event.target).closest('.dropdown_menu_button').length && !$(event.target).closest('.dropdown menu_button ul').length) {
            $('.dropdown_menu_button ul').hide();
            $('.dropdown_menu_button').removeClass('um-pressed');
        };
    });
    jQuery.validator.addMethod("complete_url", function(val, elem) {
        // if no url, don't do anything
        if (val.length == 0) { return true; }
     
        // if user has not entered http:// https:// or 
        // ftp:// assume they mean http://
        if(!/^(https?|ftp):\/\//i.test(val)) {
            val = 'http://'+val; // set both the value
            $(elem).val(val); // also update the form element
        }
        // now check if valid url
        // http://docs.jquery.com/Plugins/Validation/Methods/url
        // contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
        return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&amp;'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(val);
    }, "The url you entered is invalid.")
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
    }, "One of the emails is invalid.");
    jQuery.validator.addMethod('isMITEmail', function(value, element) {
        // If testing, allow umeqo.com emails as well.
        if (DEBUG)
               return (value.length - "mit.edu".length) == value.indexOf("mit.edu") || (value.length - "umeqo.com".length) == value.indexOf("umeqo.com");
        else
            return (value.length - "mit.edu".length) == value.indexOf("mit.edu");
    });
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
