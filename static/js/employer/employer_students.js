var window_height_min = 580;
    
var xhr = null;
var comment_xhr = null;
var filtering_ajax_request = null;

function get_current_resume_book_size(){
    return parseInt($("#students_in_resume_book_num").text());
}

function handle_resume_book_student_list_click(rb_id) {
    var li = $("#id_student_list").multiselect("widget").find("input[value='" + rb_id + "']");
    if (li.length!=0) {
        li.click();
    } else {
        initiate_ajax_call();
    }
}

function show_current_resume_book_contents(e) {
    $("#id_student_list").multiselect("widget").find("input[title='" + IN_RESUME_BOOK_STUDENT_LIST + "']").click();
    e.preventDefault();
}
function show_current_resume_book_contents_dialog(e) {
    $(".dialog").remove();
    show_current_resume_book_contents(e);
}
    
function handle_student_toggle_star() {
    var container = this;
    var student_id = $(this).attr('data-student-id');
    $.ajax({
        type: 'POST',
        url: STUDENTS_TOGGLE_STAR_URL,
        dataType: "json",
        data: {
            'student_id': student_id
        },
        beforeSend: function (jqXHR, settings) {
            place_tiny_ajax_loader(container);
        },
        success: function (data) {
            if (data.action==STARRED) {
                   $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_id + "]").text() + " has been starred.</p>");
                $(container).html(STARRED_IMG);
            } else {
                   $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_id + "]").text() + " has been unstarred.</p>");
                $(container).html(UNSTARRED_IMG);
            }
        },
        error: errors_in_message_area_handler
    });
}

function handle_students_add_star(e) {
    student_ids = [];
    $(".student_checkbox").each(function (el) {
        if (this.checked) {
            student_ids.push($(this).attr('data-student-id'));
        }
    });
    if (student_ids.length) { 
        $.ajax({
            type: 'POST',
            url: STUDENTS_ADD_STAR_URL,
            dataType: "json",
            data: {
                'student_ids': student_ids.join('~')
            },
            beforeSend: function (jqXHR, settings) {
                $(student_ids).each(function () {
                    place_tiny_ajax_loader(".student_toggle_star[data-student-id=" + this + "]");
                });
            },
            success: function (data) {
                $(student_ids).each(function () {
                    $(".student_toggle_star[data-student-id=" + this + "]").html(STARRED_IMG);
                });
                if (student_ids.length == 1) {
                    $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_ids[0] + "]").text() + " has been starred.</p>");
                } else {
                    $("#message_area").html("<p>" + student_ids.length + " students starred.</p>");
                }
            },
            error: errors_in_message_area_handler
        });
    } else {
        $("#message_area").html("<p>" + NO_STUDENTS_SELECTED_MESSAGE + "</p>");
    }
}

function handle_students_remove_star(e) {
    student_ids = [];
    $(".student_checkbox").each(function (el) {
        if (this.checked) {
            student_ids.push($(this).attr('data-student-id'));
        }
    });
    if (student_ids.length) { 
        $.ajax({
            type: 'POST',
            url: STUDENTS_REMOVE_STAR_URL,
            dataType: "json",
            data: {
                'student_ids': student_ids.join('~')
            },
            beforeSend: function (jqXHR, settings) {
                $(student_ids).each(function () {
                    place_tiny_ajax_loader(".student_toggle_star[data-student-id=" + this + "]");
                });
            },
            success: function (data) {
                $(student_ids).each(function () {
                    $(".student_toggle_star[data-student-id=" + this + "]").html(UNSTARRED_IMG);
                });
                if (student_ids.length == 1) {
                    $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_ids[0] + "]").text() + " has been unstarred.</p>");
                } else {
                    $("#message_area").html("<p>" + student_ids.length + " students unstarred.</p>");
                }
            },
            error: errors_in_message_area_handler
        });
    } else {
        $("#message_area").html("<p>" + NO_STUDENTS_SELECTED_MESSAGE + "</p>");
    }
}

function handle_students_invite_click(e) {
    student_ids = [];
    $(".student_checkbox").each(function (el) {
        if (this.checked) {
            student_ids.push($(this).attr('data-student-id'));
        }
    });
    if (student_ids.length) {   
        $.ajax({
            url: EVENTS_LIST_URL, 
            success: function (events) {
                var dialog = $('<div class="dialog"></div>').dialog({
                    autoOpen: false,
                    title: "Choose an Upcoming Event or Deadline",
                    dialogClass: "event_invitation_dialog",
                    modal: true,
                    width: 550,
                    resizable: false
                });
                if (events.length == 0) {
                    dialog.html('<span id="student_invite_no_events" class="nowrap">You have no upcoming events or deadlines! <a href="' + EVENT_NEW_URL + '">Create one</a>.</span>');
                } else {
                    var students_invite_events = $('<ul id="student_invite_events"></ul>');
                    $.each(events, function (k,event) {
                        var ispublic = event.is_public ? 1 : 0;
                        var student_ids_text = student_ids.join('~');
                        var link = $('<a data-multiple="' + student_ids_text + '" data-eventname="' + event.name + '" data-ispublic="' + ispublic + '" data-eventid="' + event.id + '" class="event_invite_link" href="#"></a>');
                        var linkText;
                        if (!ispublic) {
                            linkText = event.name + ' [private]';
                        } else {
                            linkText = event.name + ' [public]';
                        }
                        if (event.invited) {
                            linkText = linkText + ' (<strong>already invited</strong>)';
                        }
                        link.html(linkText);

                        var list_item = $('<li></li>');
                        students_invite_events.append(list_item.append(link));
                    });
                    dialog.append(students_invite_events);
                }
                dialog.dialog('open');
            },
            error: errors_in_message_area_handler
        });
    } else {
        $("#message_area").html("<p>" + NO_STUDENTS_SELECTED_MESSAGE + "</p>");
    }
}
function enforce_resume_book_size_limit(){
    if (get_current_resume_book_size() < RESUME_BOOK_CAPACITY){
        $(".resume_book_current_toggle_student div").each( function(){
            $(this).removeClass("resume_book_capacity_reached");
        });
        if($("#resume_book_current_add_students").hasClass("resume_book_capacity_reached_gray_button")){
            $("#resume_book_current_add_students").removeClass("resume_book_capacity_reached_gray_button");
        }
        if($("#resume_book_current_add_students").hasClass("disabled")){
            $("#resume_book_current_add_students").removeClass("disabled");
        }
    }else{
        $(".sprite-plus").each( function(){
            if(!$(this).hasClass("resume_book_capacity_reached")){
                $(this).addClass("resume_book_capacity_reached");
            }
        });
        if(!$("#resume_book_current_add_students").hasClass("resume_book_capacity_reached_gray_button")){
            $("#resume_book_current_add_students").addClass("resume_book_capacity_reached_gray_button");
        }
        if(!$("#resume_book_current_add_students").hasClass("disabled")){
            $("#resume_book_current_add_students").addClass("disabled");
        }
    }
}
function handle_resume_book_students_remove(e) {
    student_ids = [];
    $(".student_checkbox").each(function (el) {
        if (this.checked) {
            student_ids.push($(this).data('student-id'));
        }
    });
    if (student_ids.length) {
        $.ajax({
            type: 'POST',
            url: RESUME_BOOK_CURRENT_REMOVE_STUDENTS_URL,
            dataType: "json",
            data: {
                'student_ids': student_ids.join('~')
            },
            beforeSend: function (jqXHR, settings) {
                $(student_ids).each(function () {
                    place_tiny_ajax_loader(".resume_book_current_toggle_student[data-student-id=" + this + "]");
                });
            },
            success: function (data) {
                if (student_ids.length == 1) {
                    $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_ids[0] + "]").text() + " removed from resume book.</p>");
                } else {
                    $("#message_area").html("<p>" + student_ids.length + " students removed from resume book.</p>");
                }
                update_resume_book_contents_summary();
                if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
                    initiate_ajax_call();
                }else{
                    $(student_ids).each(function () {
                        $(".resume_book_current_toggle_student[data-student-id=" + this + "]").html(ADD_TO_RESUME_BOOK_IMG);
                    });
                }
            },
            error: errors_in_message_area_handler
        });
    } else {
        $("#message_area").html("<p>" + NO_STUDENTS_SELECTED_MESSAGE + "</p>");
    }
}

function handle_resume_book_students_add(e) {
    if(!$(this).hasClass("disabled")){
        student_ids = [];
        $(".student_checkbox").each(function (el) {
            if (this.checked) {
                student_ids.push($(this).data('student-id'));
            }
        });
        if (student_ids.length){
            if (student_ids.length > RESUME_BOOK_CAPACITY - get_current_resume_book_size()){
                $("#message_area").html("<p>Not enough room in resume book for " + student_ids.length + " students.</p>");
            } else{
                $.ajax({
                    type: 'POST',
                    url: RESUME_BOOK_CURRENT_ADD_STUDENTS_URL,
                    dataType: "json",
                    data: {
                        'student_ids': student_ids.join('~')
                    },
                    beforeSend: function (jqXHR, settings) {
                        $(student_ids).each(function () {
                            place_tiny_ajax_loader(".resume_book_current_toggle_student[data-student-id=" + this + "]");
                        });
                    },
                    success: function (data) {
                        update_resume_book_contents_summary();
                        $(student_ids).each(function () {
                            $(".resume_book_current_toggle_student[data-student-id=" + this + "]").html(REMOVE_FROM_RESUME_BOOK_IMG);
                            if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
                                $(".student_main_info[data-student-id=" + this + "]").css({'opacity': "1", 'background':'#FFF'});
                            }
                        });
                        if (student_ids.length == 1) {
                            $("#message_area").html("<p>" + $(".student_name[data-student-id=" + student_ids[0] + "]").text() + " added to resume book.</p>");
                        } else {
                            $("#message_area").html("<p>" + student_ids.length + " students added to resume book.</p>");
                        }
                    },
                    error: errors_in_message_area_handler
                });
            }
        } else {
            $("#message_area").html("<p>" + NO_STUDENTS_SELECTED_MESSAGE + "</p>");
        }
    }
}

function handle_resume_book_student_toggle(e) {
    if (!$(this).children('div').hasClass("resume_book_capacity_reached")){
        var that = this;
        var student_id = $(this).attr('data-student-id');
        $.ajax({
            type: 'POST',
            url: RESUME_BOOK_CURRENT_STUDENT_TOGGLE_URL,
            dataType: "json",
            beforeSend: function (arr, $form, options) {
                place_tiny_ajax_loader(that);
            },
            data: {
                'student_id': student_id
            },
            success: function (data) {
                update_resume_book_contents_summary();
                if (data.action==ADDED) {
                    $(that).html(REMOVE_FROM_RESUME_BOOK_IMG);
                    $("#message_area").html("<p>" + $(that).attr('data-student-name') + " added to resume book.</p>");
                } else {
                    $(that).html(ADD_TO_RESUME_BOOK_IMG);
                    $("#message_area").html("<p>" + $(that).attr('data-student-name') + " removed from resume book.</p>");
                    
                    if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
                        initiate_ajax_call();
                    }
                }
            },
            error: errors_in_message_area_handler
        });
    }
}

function handle_student_event_attendance_hover() {
    var dropdown = $(this).next(".student_event_attendance_bubble");
    if (dropdown.length == 0) {
        $(this).after('<div class="student_event_attendance_bubble"></div>');
        $(".student_event_attendance_bubble").css('left', $(this).position().left);
        place_tiny_ajax_loader('.student_event_attendance_bubble');
        if (xhr && xhr.readystate != 4) { xhr.abort(); }
        xhr = $.ajax({
            type: 'GET',
            url: STUDENT_EVENT_ATTENDANCE_URL,
            data: {
                'student_id': $(this).attr("data-student-id")
            },
            dataType: "html",
            success: function (data) {
                $(".student_event_attendance_bubble").html(data);
            },
            error: errors_in_message_area_handler
        });
    } else {
        dropdown.eq(0).remove();
    }
}

function save_student_comment(student_id, comment) {
     if (comment_xhr && comment_xhr.readystate != 4) { comment_xhr.abort(); }  
     comment_xhr = $.ajax({
        type: 'POST',
        url: STUDENT_COMMENT_URL,
        dataType: "json",
        data: {
            'student_id': student_id,
            'comment': comment
        },
        success: function (data) {
            $(".saved_message[data-student-id=" + student_id + "]").removeClass('hid');
            window.setTimeout(function () {
                $(".saved_message[data-student-id=" + student_id + "]").addClass('hid');
            }, 3000);
        },
        error: errors_in_message_area_handler
    });
}

function update_resume_book_contents_summary() {
    $.ajax({
        type: 'POST',
        url: RESUME_BOOK_CURRENT_SUMMARY_URL,
        dataType: "html",
        success: function (data) {
            $("#current_resume_book_contents_section").html(data);
            if (get_current_resume_book_size() > 0 ) {
                $(".deliver_resume_book_link").removeAttr("disabled");
            } else {
                $(".deliver_resume_book_link").attr("disabled", "disabled");
            }
            enforce_resume_book_size_limit();
        },
        error: errors_in_message_area_handler
    });
}

function handle_results_menu_toggle_details_button_click() {
    if ( $("#results_menu_toggle_details span").html()=="Show All Details") {
        $(".student_toggle_detailed_info_link").html(HIDE_DETAILS_LINK);
        $(".student_detailed_info").slideDown('slow');
        $("#results_menu_toggle_details span").html("Hide All Details");
    } else {
        $(".student_toggle_detailed_info_link").html(SHOW_DETAILS_LINK);
        $(".student_detailed_info").slideUp('slow');
        $("#results_menu_toggle_details span").html("Show All Details");
    }
}

function handle_results_menu_starred_click(e) {
    $(".sprite-star").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', true);
    });
    $(".sprite-star-empty").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', false);
    });
}

function handle_results_menu_not_starred_click(e) {
    $(".sprite-star").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', false);
    });
    $(".sprite-star-empty").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', true);
    });
}

function handle_results_menu_in_resume_book_click(e) {
    $(".sprite-plus").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', false);
    });
    $(".sprite-cross").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', true);
    });
}

function handle_results_menu_not_in_resume_book_click(e) {
    $(".sprite-plus").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', true);
    });
    $(".sprite-cross").each(function () {
        var id = $(this).parent('a').attr('data-student-id');
        $(".student_checkbox[data-student-id=" + id  + "]").attr('checked', false);
    });
}
        
function handle_results_menu_checkbox_click(e) {
    if ($("#results_menu_checkbox").prop('checked')) {
        $(".student_checkbox").not(':checked').each(function () {
            $(this).prop('checked', true);
        });
    }else{
        $(".student_checkbox:checked").each(function () {
            $(this).prop('checked', false);
        });
    }
    e.stopPropagation();
}

function handle_menu_all_on_page_click() {
    $(".student_checkbox").not(':checked').each(function () {
        $(this).attr('checked', true);
    });
}

function handle_page_link_click() {
    page = $(this).attr("id").substring(5);
    initiate_ajax_call();
}

function initiate_search() {
    query = $("#query_field").val().replace(/[^a-z@.-_\d ]+/ig,'');
    initiate_ajax_call();
}

function initiate_ajax_call() {
    if (xhr && xhr.readystate != 4) { xhr.abort(); }
    $("#message_area").html("");
    $("#results_block_content").css('opacity', 0.25);
    $("#results_block_content").css('zoom', 1);
    $("#results_block_content").css('filter', 'progid:DXImageTransform.Microsoft.Alpha(Opacity=25)');
    $("#results_block_content").css('-ms-filter', '"progid:DXImageTransform.Microsoft.Alpha(Opacity=25)"');
    $("#results_block_info_section").css('display', 'block');
    $("#results_block_info").html(LONG_HORIZONTAL_AJAX_LOADER);
    $('.student_event_attendance').die('hover');
    
    var error_dialog_timeout = setTimeout(function () {
        $("#results_block_info").prepend(two_line_long_load_message);
    }, LOAD_WAIT_TIME);
    
    data = {
        'page': page,
        'student_list': student_list,
        'student_list_id': student_list_id,
        'older_than_21' : older_than_21,
        'ordering': ordering,
        'results_per_page': results_per_page
        }
 	
 	if (query)
 		data['query'] = query
 	if (min_gpa != 0)
 		data['gpa'] = min_gpa
 	if (min_act != 0)
 		data['act'] = min_act
 	if (min_sat_t != 600)
       data['sat_t'] = min_sat_t
    if (min_sat_m != 200)
    	data['sat_m'] = min_sat_m
    if (min_sat_v != 200)
    	data['sat_v'] = min_sat_v
    if (min_sat_w != 200)
    	data['sat_w'] = min_sat_w
	if (courses.length != 0)
		data['courses'] = courses.join('~')
	if (school_years.length != 0)
		data['school_years'] = school_years.join('~')
	if (graduation_years.length != 0)
		data['graduation_years'] =  graduation_years.join('~')
	if (employment_types.length != 0)
        data['employment_types'] = employment_types.join('~')
    if (previous_employers.length != 0)
        data['previous_employers'] = previous_employers.join('~')
    if (industries_of_interest.length != 0)
        data['industries_of_interest'] = industries_of_interest.join('~')
    if (campus_orgs.length != 0)
        data['campus_orgs'] = campus_orgs.join('~')
    if (languages.length != 0)
        data['languages'] = languages.join('~')
    if (countries_of_citizenship.length != 0)
    	data['countries_of_citizenship'] = countries_of_citizenship.join('~')
        
    xhr = $.ajax({
        type: 'GET',
        url: STUDENTS_URL,
        dataType: "html",
        data: data,
        complete: function (jqXHR, textStatus) {
            clearTimeout(error_dialog_timeout);
        },
        success: function (data) {
            $('#results_block_content').html(data);
            
            $('.student_event_attendance').live('hover', handle_student_event_attendance_hover);
            
            $(".student_comment").autoResize({
                animateDuration : 0,
                extraSpace : 18
            });

            $(".student_comment").placeholder();
    
            // Bring the opacity back to normal and hide the ajax loader
            $("#results_block_content").css('opacity', 1);
            $("#results_block_info_section").css('display', 'none');
        },
        error: errors_in_message_area_handler
    });
}

var handle_window_scroll = null;
function set_up_side_block_scrolling() {
    var el = $('#side_block_area');
    var elpos_original = el.offset().top;
    var scroll_side_block = function ( ) {
        var elpos = el.offset().top;
        var windowpos = $(window).scrollTop();
        var finaldestination = windowpos;
        if (windowpos<elpos_original) {
            finaldestination = elpos_original;
            el.stop(true).animate({
                'top' : 0
            }, 400, 'easeInOutExpo');
        } else {
            el.stop(true).animate({
                'top' : windowpos-70
            }, 400, 'easeInOutExpo');
        }
    };

    var handle_window_scroll = function () {
        if (this.scrollTO) {
            clearTimeout(this.scrollTO);
        }
        this.scrollTO = setTimeout(function () {
            $(this).trigger('scrollEnd');
        }, 100);
    };
    
    $(window).bind('scroll', handle_window_scroll);
    $(window).bind('scrollEnd', scroll_side_block);
}

var min_gpa = 0,
min_act = 0,
min_sat_t = 600,
min_sat_m = 200,
min_sat_v = 200,
min_sat_w = 200,
page = 1,
courses = new Array(),
school_years = new Array(),
graduation_years = [],
previous_employers = [],
industries_of_interest = [],
employment_types = [],
languages = [],
countries_of_citizenship = [],
campus_orgs = [],
student_list = null,
student_list_id = null,
ordering = null,
results_per_page = null,
older_than_21 = null;
    
$(document).ready(function () {
    student_list = $("#id_student_list option:selected").text(),
    student_list_id = $("#id_student_list option:selected").val(),
    ordering = $("#id_ordering option:selected").val(),
    results_per_page = $("#id_results_per_page option:selected").val(),
    older_than_21 = $("#id_older_than_21 option:selected").val();

    $(window).resize(function () {
        if (this.resizeTO) {
            clearTimeout(this.resizeTO);
        }
        this.resizeTO = setTimeout(function () {
            $(this).trigger('resizeEnd');
        }, 500);
    });
   ~
    $(window).bind('resizeEnd', function () {
        if ($(window).height()>window_height_min) { 
            set_up_side_block_scrolling();
            $(window).trigger('scroll');
        } else {
            $('#side_block_area').stop(true).css('top', 0);
            $(window).unbind('scroll', handle_window_scroll); 
        }
    });
    
    $("#results_menu_in_resume_book").live('click', handle_results_menu_in_resume_book_click);
    $("#results_menu_not_in_resume_book").live('click', handle_results_menu_not_in_resume_book_click);
    $("#results_menu_not_starred").live('click', handle_results_menu_not_starred_click);
    $("#results_menu_starred").live('click', handle_results_menu_starred_click);
    $("#results_menu_all_on_page").live('click', handle_menu_all_on_page_click);
    $("#results_menu_checkbox").live('click', handle_results_menu_checkbox_click);
    $("#show_current_resume_book_contents").live('click', show_current_resume_book_contents);
    $("#show_current_resume_book_contents_dialog").live('click', show_current_resume_book_contents_dialog );
    
    $(".student_toggle_star").live('click', handle_student_toggle_star);
    $("#students_add_star").live('click', handle_students_add_star);
    $("#students_remove_star").live('click', handle_students_remove_star);
    $("#students_invite").live('click', handle_students_invite_click);
    
    $(".resume_book_current_toggle_student").live('click', handle_resume_book_student_toggle);
    $("#resume_book_current_add_students").live('click', handle_resume_book_students_add);
    $("#resume_book_current_remove_students").live('click', handle_resume_book_students_remove);
    $("#results_menu_toggle_details").live('click', handle_results_menu_toggle_details_button_click );

    $("#search_form_submit_button").click(initiate_search);
    $(".page_link").live('click', handle_page_link_click);
    $("#initiate_ajax_call").live('click', initiate_ajax_call);
    
    $("#query_field").val(query);
    var timeoutID;
    
    $('#query_field').keydown(function () {
        if (typeof timeoutID!='undefined') {
            window.clearTimeout(timeoutID);
        }
        timeoutID = window.setTimeout(initiate_search, 1000);
    });
    
    $('.student_comment').live('keydown', function () {
        var id = $(this).attr('data-student-id');
        var textarea = this;
        if (typeof timeoutID!='undefined') {
            window.clearTimeout(timeoutID);
        }
        timeoutID = window.setTimeout(function () {
            save_student_comment(id, $(textarea).val());
        }, 500);
    });
    if ($(window).height()>window_height_min) {
        set_up_side_block_scrolling();
    }
    $("#id_student_list").multiselect({
        header: false,
        multiple: false,
        selectedList: 1,
        height:252,
        classes: 'student_list_multiselect',
        minWidth: multiselectMinWidth,
        click: function (event, ui) {
            student_list = ui.text;
            student_list_id = ui.value;
            initiate_ajax_call();
        },
        beforeoptgrouptoggle: function (e, ui) {
            return false;
        }
    });

    var slt = get_parameter_by_name("slt");
    if (slt) {
        var st = $("#id_student_list").multiselect("widget").find("input[title='" + decodeURIComponent(slt)  + "']");
        if (st.length != 0) {
            st.click();
        } else {
            initiate_ajax_call();
        }
    } else {
        var isl = get_parameter_by_name("isl");
        if (isl) {
            handle_resume_book_student_list_click(isl);
        } else {
            initiate_ajax_call();
        }
    }

    update_resume_book_contents_summary();
    
    $('.student_invite_to_event_span').live('mouseover', function () {
        if (!$(this).data('init')) {
            $(this).data('init', true);
            var that = this;
            $(this).hoverIntent({
	            sensitivity:2,
	            over: function () {
	                $(that).append('<div class="events_dropdown"></div>');
	                place_tiny_ajax_loader('.events_dropdown');
	                if (xhr && xhr.readystate != 4) { xhr.abort(); }
	                xhr = $.ajax({
	                    url: EVENTS_LIST_URL, 
	                    data: {"student_id": $(this).attr('data-studentid')}, 
	                    success: function (events) {
	                        var dropdown = $(".events_dropdown");
	                        if (events.length == 0) {
	                            dropdown.html('<span class="nowrap">You have no upcoming events! <a href="' + EVENT_NEW_URL + '">Create one</a>.</span>');
	                        } else {
	                            dropdown.html('');
	                            $.each(events, function (k,event) {
	                                var ispublic = event.is_public ? 1 : 0;
	                                var link = $('<a data-eventname="' + event.name + '" data-ispublic="' + ispublic + '" data-eventid="' + event.id + '" class="event_invite_link" href="#"></a>');
	                                var linkText;
	                                if (!ispublic) {
	                                    linkText = event.name + ' [private]';
	                                } else {
	                                    linkText = event.name + ' [public]';
	                                }
	                                if (event.invited) {
	                                    linkText = linkText + ' (<strong>already invited</strong>)';
	                                }
	                                link.html(linkText);
	                                dropdown.append(link);
	                            });
	                        }
	                    },
	                    error: errors_in_message_area_handler
	                });
	            },
	            out: function () {
	                $(this).children('.events_dropdown').remove();
	            }
            });
            $(this).trigger('mouseover');
        }
    });
    $('.student_invite_to_event_span .student_invite_to_event_link').live('click', function (e) {
        e.preventDefault();
    });
    
    $(".student_resume_link").live('click', function () {
        $.ajax({
            type: 'POST',
            url: STUDENT_INCREMENT_RESUME_VIEW_COUNT_URL,
            data: {
                'student_id': $(this).attr("data-student-id")
            }
        });
    });
    
    $('.event_invite_link').live('click', function (e) {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var student_name;
        var student_id;
        if ($(this).data('multiple')) {
            student_name = "The selected students";
            student_ids = $(this).data('multiple');
        } else {
            student_name = $(this).closest('span').data('studentname');
            student_ids = $(this).closest('span').data('studentid');
        }
        var event_name = $(this).data('eventname');
        var event_id = $(this).data('eventid');
        var is_public = $(this).data('ispublic') == 1;
        var that = this;
        var title, extra_text;
        if (is_public) {
            if ($(this).data('multiple')) {
                title = "Send invite to students?";
            } else {
                title = "Send invite to student?";
            }
            extra_text = "This event is <strong>public</strong>. Students that aren't explicitly invited can see it as well.";
        } else {
            if ($(this).data('multiple')) {
                title = "Send private invite to students?";
            } else {
                title = "Send private invite to student?";
            }
            extra_text = "This event is <strong>private</strong> and only invited students will be able to see it.";
        }
        var invite_dialog = $('<div id="invite-dialog" title="' + title + '"></div>');
        var invite_text;
        if ($(this).data('multiple')) {
            invite_text = "Hi there, I'd like to invite you to our event.";
        } else {
            invite_text = "Hi " + student_name + ", I'd like to invite you to our event.";
        }
        var msg_input = $('<textarea id="invite_text">' + invite_text + '</textarea>');
        invite_dialog.html('<p>' + student_name + ' will get an invite for your event, <strong>' + event_name + '</strong>, with your name and company included with the message below. <em>Try to make your message as personalized as possible - students will be more likely to respond!</em></p>');
        invite_dialog.append(msg_input);
        invite_dialog.append('<p>' + extra_text + '</p>');
        invite_dialog.dialog({
            height: 'auto',
            minHeight: 0,
            width: 415,
            title: title,
            resizable: false,
            modal: true,
            buttons: {
                "Send invite": function () {
                    $("#message_area").html('<p>Sending invite...</p>');
                    $.post(EVENT_INVITE_URL, {
                        event_id: event_id,
                        student_ids: student_ids,
                        message: $('#invite_text').val()
                    }, function (data) {
                        $("#message_area").html('<p>' + data.message + '</p>');
                    }).error(function () {
                        $("#message_area").html('<p>Invite could not be sent. Please try again later.</p>');
                    });
                    $('.ui-dialog').dialog("close").remove();
                },
                Cancel: function () {
                    $(that).dialog("close");
                    invite_dialog.remove();
                }
            }
        });
        $('#invite_text').focus().select();
        e.preventDefault();
    });
    
    $("#query_field").placeholder();
    $("#side_block_area .slider_section input.readonly").attr("readonly", "readonly");
});