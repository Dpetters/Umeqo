$(document).ready(function(){

    $("label[for=id_school_years]").parent().next().children(':eq(0)').multiselect({
        height:140,
        noneSelectedText: 'select school years',
        checkAllText: "All",
        uncheckAllText: "None",
    });

    $("label[for=id_graduation_years]").parent().next().children(':eq(0)').multiselect({
        height:120,
        noneSelectedText: 'select graduation years',
        checkAllText: "All",
        uncheckAllText: "None",
    });

    $("label[for=id_majors]").parent().next().children(':eq(0)').multiselect({
        height:200,
        noneSelectedText: 'select course',
        checkAllText: "All",
        uncheckAllText: "None",
    }).multiselectfilter();

    $("label[for=id_languages]").parent().next().children(':eq(0)').multiselect({
        height:200,
        noneSelectedText: 'select languages',
        checkAllText: "All",
        uncheckAllText: "None",
    }).multiselectfilter();

    $("label[for=id_campus_orgs]").parent().next().children(':eq(0)').multiselect({
        height:200,
        noneSelectedText: 'select campus organizations',
        checkAllText: "All",
        uncheckAllText: "None",
    }).multiselectfilter();

    $("label[for=id_industries_of_interest]").parent().next().children(':eq(0)').multiselect({
        height:200,
        noneSelectedText: 'select industries',
        checkAllText: "All",
        uncheckAllText: "None",
    }).multiselectfilter();

    $("label[for=id_previous_employers]").parent().next().children(':eq(0)').multiselect({
        height:200,
        noneSelectedText: 'select employers',
        checkAllText: "All",
        uncheckAllText: "None",
    }).multiselectfilter();

    $("label[for=id_looking_for_internship]").parent().next().children(':eq(0)').multiselect({
        noneSelectedText: "select",
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("label[for=id_looking_for_fulltime]").parent().next().children(':eq(0)').multiselect({
        noneSelectedText: "select",
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("label[for=id_older_than_21]").parent().next().children(':eq(0)').multiselect({
        noneSelectedText: "select",
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
    });

    $("label[for=id_citizen]").parent().next().children(':eq(0)').multiselect({
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
            sat: {
                range: [600, 2400],
                maxlength: 4
            },
            act: {
                range: [0, 36],
                maxlength: 2
            }
        },
        messages: {
            gpa: 'GPA must be between 0 and 5.0',
            sat: 'SAT must be between 600 and 2400',
            act: 'ACT must be between 0 and 36'
        }
    });
})