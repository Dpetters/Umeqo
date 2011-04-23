/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

    $("#id_hours, #id_minutes").bind('change', function() {
        new_event_form_validator.element("#id_days");
    });
    var event_rules = {
        name:{
            required: true,
        },
        start_datetime_0:{
            required: true,
        },
        type:{
            required:true,
        },
        location:{
            required:{
                depends: function(element) {
                    return $("#id_type option:selected").text() != "Deadline";
                }
            },
        }
    };

    var deadline_rules = {
        name:{
            required: true,
        },
        start_datetime_0:{
            required: true,
        },
        type:{
            required:true,
        },
    };

    var external_rsvp_rules = {
        external_site:{
            required:true,
        }
    };

    var email_rsvp_rules = {
        email:{
            required:true,
        }
    };

    function addRules(rulesObj) {
        for (item in rulesObj) {
            $('#id_'+item).rules('add',rulesObj[item]);
        }
    }

    function removeRules(rulesObj) {
        for (item in rulesObj) {
            $('#id_'+item).rules('remove');
        }
    }

    $("label[for=id_description]").css('padding-left', '0px');

    $("#id_type").change( function() {
        if($("#id_type option:selected").text() === "Deadline") {
            $("label[for=id_name]").text("Deadline Name");
            $("label[for=id_description]").text("Deadline Description");
            $('.event_only_field').hide();
        } else {
            $('.event_only_field').each( function() {
                if($(this).hasClass("external_rsvp_only_field")) {
                    if($("#id_rsvp_type option:selected").text() === "On External Website")
                        $(this).show();
                } else if ($(this).hasClass("email_rsvp_only_field")) {
                    if($("#id_rsvp_type option:selected").text() === "By Email")
                        $(this).show();
                } else
                    $(this).show();
            });
        }
    });
    $("#id_rsvp_type").change( function() {
        if($("#id_rsvp_type option:selected").text() === "On External Website") {
            $('.external_rsvp_only_field').show();
            $('.email_rsvp_only_field').hide();
            removeRules(email_rsvp_rules);
            addRules(external_rsvp_rules);
        } else if ($("#id_rsvp_type option:selected").text() === "By Email") {
            $('.external_rsvp_only_field').hide();
            $('.email_rsvp_only_field').show();
            addRules(email_rsvp_rules);
            removeRules(external_rsvp_rules);
        } else {
            $('.external_rsvp_only_field, .email_rsvp_only_field').hide();
            removeRules(external_rsvp_rules);
            removeRules(email_rsvp_rules);

        }
    });
    var new_event_form_validator = $("#new_event_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors,
    });

    addRules(event_rules);
    format_required_labels();
    align_form();

    $('.external_rsvp_only_field, .email_rsvp_only_field').hide();

    $("#id_audience").multiselect({
        noneSelectedText: 'select school years',
        minWidth: 204,
        height:146
    });

});