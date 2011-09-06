$(document).ready(function() {
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
                        if ('image' in data.errors){
                            $($("#id_image").prevAll(".errorspace")[0]).html("<label class='error' for='image'>" +data.errors["image"] + "</label>");
                        } else {
                            place_table_form_errors("#profile_form", data.errors);   
                        }
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
            type : {
                required : true
            },
            email : {
                email : true
            },
            website : {
                complete_url : true
            }
        },
        messages : {
            website : INVALID_URL,
            email : {
                email : INVALID_EMAIL
            },
        }
    });
});