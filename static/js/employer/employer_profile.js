$(document).ready(function() {
    $("#profile_form").submit(function() {
        console.log("herro");
        for (instance in CKEDITOR.instances){
            console.log("wow")
            CKEDITOR.instances[instance].updateElement();
        }
    });

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
            main_contact : {
                required : true
            },
            main_contact_email : {
                required : true,
                email : true
            },
            main_contact_phone : {
                phoneUS : true
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
            main_contact : MAIN_CONTACT_REQUIRED,
            main_contact_email : {
                required : MAIN_CONTACT_EMAIL_REQUIRED,
                email : INVALID_EMAIL
            },
            main_contact_phone : {
                phoneUS : INVALID_PHONE
            }
        }
    });
    // Back buttons do not need to run validation
    $("#pg2 .open0").click(function() {
        accordion.accordion("activate", 0);
        current = 0;
    });
    // Next buttons need to run validation
    $("#pg1 .open1").click(function() {
        if(v.form()) {
            accordion.accordion("activate", 1);
            current = 1;
        }
    });
    
});
