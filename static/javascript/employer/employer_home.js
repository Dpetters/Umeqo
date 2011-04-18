/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function () {

    var open_default_filtering_parameters_dialog = function () {
        var $dialog = $('<div></div>')
        .dialog({
            autoOpen: false,
            title: "Choose Your Default Filtering Parameters",
            modal: true,
            dialogClass: "setup_default_filtering_parameters_dialog",
            width:840,
            resizable: false,
        });
        $dialog.dialog('open');
        return $dialog;
    };
    $('#open_default_parameters_form_link').live('click', function () {
        var $default_filtering_parameters_dialog = open_default_filtering_parameters_dialog();

        $default_filtering_parameters_dialog.html(ajax_loader);
        $default_filtering_parameters_dialog.load('/employer/setup-default-filtering-parameters/', function () {

            $default_filtering_parameters_dialog.dialog('option', 'position', 'center');

            $(window).resize( function() {
                $default_filtering_parameters_dialog.dialog('option', 'position', 'center');
            });
            format_required_labels();

            align_form("#default_filtering_parameters_form_left_half_first_section");
            align_form("#default_filtering_parameters_form_left_half_second_section");
            align_form("#default_filtering_parameters_form_right_half");

            $("label[for=id_school_years]").next().multiselect({
                height:140,
                noneSelectedText: 'select school years',
                checkAllText: "All",
                uncheckAllText: "None",
            });

            $("label[for=id_graduation_years]").next().multiselect({
                height:120,
                noneSelectedText: 'select graduation years',
                checkAllText: "All",
                uncheckAllText: "None",
            });

            $("label[for=id_majors]").next().multiselect({
                height:200,
                noneSelectedText: 'select course',
                checkAllText: "All",
                uncheckAllText: "None",
            }).multiselectfilter();

            $("label[for=id_languages]").next().multiselect({
                height:200,
                noneSelectedText: 'select languages',
                checkAllText: "All",
                uncheckAllText: "None",
            }).multiselectfilter();

            $("label[for=id_campus_orgs]").next().multiselect({
                height:200,
                noneSelectedText: 'select campus organizations',
                checkAllText: "All",
                uncheckAllText: "None",
            }).multiselectfilter();

            $("label[for=id_industries_of_interest]").next().multiselect({
                height:200,
                noneSelectedText: 'select industries',
                checkAllText: "All",
                uncheckAllText: "None",
            }).multiselectfilter();

            $("label[for=id_previous_employers]").next().multiselect({
                height:200,
                noneSelectedText: 'select employers',
                checkAllText: "All",
                uncheckAllText: "None",
            }).multiselectfilter();

            $("label[for=id_looking_for_internship]").next().multiselect({
                noneSelectedText: "select",
                height:47,
                header:false,
                minWidth:187,
                selectedList: 1,
                multiple: false
            });

            $("label[for=id_looking_for_fulltime]").next().multiselect({
                noneSelectedText: "select",
                height:47,
                header:false,
                minWidth:187,
                selectedList: 1,
                multiple: false
            });

            $("label[for=id_older_than_18]").next().multiselect({
                noneSelectedText: "select",
                height:47,
                header:false,
                minWidth:187,
                selectedList: 1,
                multiple: false
            });

            $("label[for=id_citizen]").next().multiselect({
                noneSelectedText: "select",
                height:47,
                header:false,
                minWidth:187,
                selectedList: 1,
                multiple: false
            });

            $("#default_filtering_parameters_form").validate({
                submitHandler: function (form) {
                    $(form).ajaxSubmit({
                        dataType: 'json',
                        beforeSubmit: function (arr, $form, options) {
                            show_dialog_form_submit_loader();
                        },
                        success: function (data) {
                            hide_dialog_form_submit_loader();
                            var success_message = "<br><div class='message_section'><p>Your default filtering parameters have been updated.</p><br><a id='close_dialog_link' href='javascript:void(0)'>Close Dialog</a></div>";
                            $default_filtering_parameters_dialog.html(success_message);
                            $default_filtering_parameters_dialog.dialog('option', 'position', 'center');
                            $("#close_dialog_link").live('click', function () {
                                $default_filtering_parameters_dialog.dialog('close');
                            });
                        }
                    });
                },
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_errors,
                rules: {
                    gpa: {
                        range: [0, 5.0],
                        maxlength: 4
                    },
                    sat_t: {
                        range: [600, 2400],
                        maxlength: 4
                    },
                    sat_m: {
                        range: [200, 800],
                        maxlength: 3
                    },
                    sat_w: {
                        range: [200, 800],
                        maxlength: 3
                    },
                    sat_v: {
                        range: [200, 800],
                        maxlength: 3
                    },
                    act: {
                        range: [0, 36],
                        maxlength: 2
                    }
                }
            });
        });
    });
    var search_form_validator = $("#search_form").validate({
        highlight: highlight,
        unhighlight: unhighlight,
        errorPlacement: place_errors,
        rules: {
            query: {
                required: true,
            }
        },
        messages: {
            query: "Please supply a query"
        }
    });
    
});