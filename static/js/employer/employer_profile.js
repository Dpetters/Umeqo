$(document).ready(function() {
    $("#profile_form").submit(update_ckeditors);
    $("#id_visible").switchify();
    v = $("#profile_form").validate({
        submitHandler : function(form) {
            $(form).ajaxSubmit({
                dataType : 'text',
                beforeSubmit : function(arr, $form, options) {
                    $("#profile_form input[type=submit]").attr("disabled", "disabled");
                    show_form_submit_loader("#profile_form");
                    $("#profile_form .error_section").html("");
                },
                complete : function(jqXHR, textStatus) {
                    $("#profile_form input[type=submit]").removeAttr("disabled");
                    hide_form_submit_loader("#profile_form");
                },
                success : function(data) {
                    data = $.parseJSON(data);
                    console.log(data.errors);
                    if(data.errors) {
                        place_table_form_errors("#profile_form", data.errors);
                    } else {
                        window.location.href = HOME_URL + "?msg=profile-saved";
                    }
                },
                error : errors_in_message_area_handler
            });
        },
        highlight : highlight,
        unhighlight : unhighlight,
        errorPlacement : place_table_form_field_error,
        rules : {
            name : {
                required : true
            },
            slug : {
                required : true,
                remote: {
                    dataType: 'json',
                    url: CHECK_EMPLOYER_CAMPUS_ORG_SLUG_UNIQUENESS_URL,
                    error: errors_in_message_area_handler
                }
            },
            industries : {
                required : true
            },
            description : {
                required : true
            },
            website : {
                complete_url : true
            }
        },
        messages : {
            name : NAME_REQUIRED,
            slug : {
                reguired:SLUG_REQUIRED,
                remote: SLUG_ALREADY_TAKEN
            },
            industries : INDUSTRIES_REQUIRED,
            description : DESCRIPTION_REQUIRED,
            website : INVALID_URL,
        }
    });
});