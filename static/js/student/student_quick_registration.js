var student_quick_registration_validator, action;

function open_create_student_quick_registration_dialog() {
    var create_student_quick_registration_dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        dialogClass: "student_quick_registration_dialog",
        resizable: false,
        modal: true,
        width: 505,
        close: function() {
            create_student_quick_registration_dialog.remove();
        }
    });
    create_student_quick_registration_dialog.dialog('open');
    return create_student_quick_registration_dialog;
};

$(".open_registration_help_dialog_link").live('click', function(){
    $("#student_registration_help").slideToggle();
});
function submit_student_quick_registration_form(form, ignore_unparsable_resume){
    var ignore_unparsable_resume = typeof(ignore_unparsable_resume) != 'undefined' ? ignore_unparsable_resume : false;
    
    $(form).ajaxSubmit({
        dataType: 'text',
        data:{'ignore_unparsable_resume':"false"},
        beforeSubmit: function (arr, $form, options) {
            $("#message_area").html("");
            $("#student_quick_registration_form input[type=submit]").attr("disabled", "disabled");
            show_form_submit_loader("#student_quick_registration_form");
            $("#student_quick_registration_form .error_section").html("");
        },
        complete : function(jqXHR, textStatus) {
            $("#student_quick_registration_form input[type=submit]").removeAttr("disabled");
            hide_form_submit_loader("#student_quick_registration_form");
        },
        success: function (data) {
            data = $.parseJSON(data);
            if(data.errors) {
                place_table_form_errors("#student_quick_registration_form", data.errors);
            } else {
                console.log(data.unparsable_resume);
                $.ajax({
                    url: STUDENT_QUICK_REGISTRATION_DONE_URL,
                    dataType: "html",
                    data:{'unparsable_resume':data.unparsable_resume},
                    success: function (html) {
                        create_student_quick_registration_dialog.html(html);
                    },
                    error: errors_in_message_area_handler
                });
                if (action == "rsvp"){
                    $("#rsvp_button").removeClass("student_quick_registration_link").addClass("post_quick_registration_event_action_button button-success");
                    var parent = get_parent($("#rsvp_button"));
                    var is_deadline = $(parent).data("is-deadline")=="True";
                    if(is_deadline){
                        $("#rsvp_button").text("Participating");
                    }else{
                        $("#rsvp_button").text("Attending");
                    }
                }
                $("#drop_resume_button").removeClass("student_quick_registration_link").addClass("post_quick_registration_event_action_button button-success").text("Resume Dropped");
                create_student_quick_registration_dialog.dialog("option", "title", "Account Created Successfully");
                
            }
        },
        error: errors_in_message_area_handler
    });  
};

function prefill_student_quick_registration_fields(){
    var email = $("#id_email").val();
    if (is_valid_email_address(email) && is_valid_mit_email(email)){
        $.ajax({
            url:STUDENT_INFO_URL,
            data:{'email':$("#id_email").val()},
            success:function(data){
                if (data.first_name && $("#id_first_name").val()==""){
                    $("#id_first_name").val(data.first_name);
                }
                if (data.last_name && $("#id_last_name").val()==""){
                    $("#id_last_name").val(data.last_name);
                }
                if (data.course && $("#id_first_major").val()==""){
                    $("#id_first_major").val(data.course);
                }
            }
        });
    }
}

// Get rid of resume field errors as a user selects a file
// JQuery validation doesn't respond to the change event
$("#id_resume").live('change', function() {
    student_quick_registration_validator.element("#id_resume");
});
    
$('.student_quick_registration_link').live('click', function (e) {
    action = $(this).attr("data-action");
    var next = $("input[name=next]").val();
    if (next.indexOf("?")!=-1){
        next += "&";
    }else{
        next += "?";
    }
    
    if ($(this).attr("id") == "rsvp_button"){
        $("input[name=next]").val(next + "rsvp=true")
    } else if ($(this).attr("id") == "drop_resume_button"){
        $("input[name=next]").val(next + "?drop=true")
    }
    create_student_quick_registration_dialog = open_create_student_quick_registration_dialog();
    create_student_quick_registration_dialog.dialog("option", "title", $(this).attr("data-title"));    
    create_student_quick_registration_dialog.html(DIALOG_AJAX_LOADER);
    var create_student_quick_registration_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        dataType: "html",
        data: {'action':$(this).attr("data-action"),
                'event_id':$(this).attr("data-event-id")
              },
        url: STUDENT_QUICK_REGISTRATION_URL,
        complete : function(jqXHR, textStatus) {
            clearTimeout(create_student_quick_registration_dialog_timeout);
            create_student_quick_registration_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                create_student_quick_registration_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                create_student_quick_registration_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            create_student_quick_registration_dialog.html(data);
            $("#id_looking_for").multiselect({
                noneSelectedText: 'select job types',
                checkAllText: multiselectCheckAllText,
                uncheckAllText: multiselectUncheckAllText,
                minWidth:multiselectMinWidth,
                height:'auto',
                checkAll: function(){
                    $("#id_looking_for").trigger("change");
                },
                uncheckAll: function(){
                    $("#id_looking_for").trigger("change");
                }
            }).multiselectfilter();

            var timeoutID;
            $('#id_email').keydown(function () {
                if (typeof timeoutID!='undefined') {
                    window.clearTimeout(timeoutID);
                }
                timeoutID = window.setTimeout(prefill_student_quick_registration_fields, 200);
            });
    
            student_quick_registration_validator = $("#student_quick_registration_form").validate({
                submitHandler: function (form) {
                    submit_student_quick_registration_form(form, false);
                }, 
                highlight: highlight,
                unhighlight: unhighlight,
                errorPlacement: place_table_form_field_error,
                rules: {
                    email: {
                        required: true,
                        email: true,
                        isMITEmail: true,
                        remote: {
                            dataType: 'json',
                            url: CHECK_EMAIL_AVAILABILITY_URL,
                            error: errors_in_message_area_handler
                        }
                    },
                    password: {
                        required: true,
                        minlength: PASSWORD_MIN_LENGTH
                    },
                    first_name: {
                        required: true
                    },
                    last_name: {
                        required: true
                    },
                    degree_program: {
                        required: true
                    },
                    graduation_year: {
                        required: true
                    },
                    first_major: {
                        required: true
                    },
                    gpa: {
                        required: true,
                        range: [0, 5.0],
                        maxlength: 4
                    },
                    resume:{
                        accept: "pdf"
                    },
                },
                messages: {
                    email:{
                        required: EMAIL_REQUIRED,
                        email: INVALID_EMAIL,
                        isMITEmail: MUST_BE_MIT_EMAIL,
                        remote: EMAIL_ALREADY_REGISTERED
                    },
                    password1: {
                        required: PASSWORD_REQUIRED
                    },
                    first_name: FIRST_NAME_REQUIRED,
                    last_name: LAST_NAME_REQUIRED,
                    degree_program: DEGREE_PROGRAM_REQUIRED,
                    graduation_year: GRADUATION_YEAR_REQUIRED,
                    first_major: FIRST_MAJOR_REQUIRED,
                    gpa: {
                        required: GPA_REQUIRED,
                        range: GPA_RANGE
                    },
                    resume: RESUME_REQUIRED,
                }
            });
        }
    });
    e.preventDefault();
});