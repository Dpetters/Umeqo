/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */
$(document).ready(function() {
	var no_students_selected_message = "<p>No students selected.</p>";
    var filtering_ajax_request = null;
    
    /* Filtering Variables */
    var min_gpa = 0;
    var min_act = 0;
    var min_sat_t = 600;
    var min_sat_m = 200;
    var min_sat_v = 200;
    var min_sat_w = 200;
    var page = 1;
    var student_list = $("#id_student_list option:selected").text();
    var ordering = $("#id_ordering option:selected").val();
    var results_per_page = $("#id_results_per_page option:selected").val();
    var courses = [];
    var school_years = [];
    var graduation_years = [];
    var previous_employers = [];
    var industries_of_interest = [];
    var employment_types = [];
    var languages = [];
    var countries_of_citizenship = [];
    var campus_orgs = [];
	var older_than_18 = $("#id_older_than_18 option:selected").val();
	
	function switch_to_students_in_resume_book_student_list() {
		$("#id_student_list").multiselect("widget").find("input[title='" + IN_RESUME_BOOK_STUDENT_LIST + "']").click()
	};
	
	function switch_to_students_in_resume_book_student_list_dialog() {
		deliver_resume_book_dialog.remove();
		$("#id_student_list").multiselect("widget").find("input[title='" + IN_RESUME_BOOK_STUDENT_LIST + "']").click();
	};
	
    function open_event_invitation_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Send Event Invitation",
            dialogClass: "event_invitation_dialog",
            modal:true,
            width:550,
            resizable: false,
            close: function(event, ui) {
                event_invitation_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    	
    function open_deliver_resume_book_dialog() {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:"Deliver Resume Book",
            dialogClass: "deliver_resume_book_dialog",
            modal:true,
            width:470,
            resizable: false,
            close: function(event, ui) {
                deliver_resume_book_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    function open_campus_org_info_dialog(campus_org_name) {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:campus_org_name,
            dialogClass: "campus_org_info_dialog",
            modal:true,
            width:550,
            resizable: false,
            close: function() {
                campus_org_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };
    
    function open_course_info_dialog(major_name) {
        var $dialog = $('<div class="dialog"></div>')
        .dialog({
            autoOpen: false,
            title:major_name,
            dialogClass: "course_info_dialog",
            modal:true,
            width:550,
            resizable: false,
            close: function() {
                course_info_dialog.remove();
            }
        });
        $dialog.dialog('open');
        return $dialog;
    };

    function handle_star_students_add_click(e) {
        ids = []
        $(".student_checkbox").each( function(el) {
            if (this.checked)
                ids.push($(this).attr('num'));
        });
        if(ids.length){ 
	        $.ajax({
	            type: 'POST',
	            url: "/employer/star/students/add/",
	            dataType: "json",
	            data: {
	                'student_ids': ids.join('~'),
	            },
	            beforeSend: function (jqXHR, settings) {
	                $(ids).each( function() {
	                    place_tiny_ajax_loader(".student_toggle_star_link[num=" + this + "]");
	                });
	            },
	            success: function (data) {
	                switch(data.valid) {
	                    case true:
	                        $(ids).each( function() {
	                            $(".student_toggle_star_link[num=" + this + "]").html(STARRED_IMG);
	                        });
	                        if (ids.length == 1){
                            	$("#message_area").html("<p>" + $(".student_name[num=" + ids[0] + "]").text() + " has been starred.</p>");
	                        } else {
	                    	    $("#message_area").html("<p>" + ids.length + " students starred.</p>");
	                        }
	                        break;
	                    case false:
	                    default:
	                        show_error_dialog(page_error_message);
	                        break;
	                };
	            },
	            error: function(jqXHR, textStatus, errorThrown) {
	                switch(jqXHR.status) {
	                    case 0:
	                        show_error_dialog(page_check_connection_message);
	                        break;
	                    default:
	                        show_error_dialog(page_error_message);
	                }
	            },
	        });
        } else {
        	$("#message_area").html(no_students_selected_message);
        }
	};

    function handle_star_students_remove_click(e) {
        ids = []
        $(".student_checkbox").each( function(el) {
            if (this.checked)
                ids.push($(this).attr('num'));
        });
        if(ids.length){ 
	        $.ajax({
	            type: 'POST',
	            url: "/employer/star/students/remove/",
	            dataType: "json",
	            data: {
	                'student_ids': ids.join('~'),
	            },
	            beforeSend: function (jqXHR, settings) {
	                $(ids).each( function() {
	                    place_tiny_ajax_loader(".student_toggle_star_link[num=" + this + "]");
	                });
	            },
	            success: function (data) {
	                switch(data.valid) {
	                    case true:
	                        $(ids).each( function() {
	                            $(".student_toggle_star_link[num=" + this + "]").html(UNSTARRED_IMG);
	                        });
	                        if (ids.length == 1){
                            	$("#message_area").html("<p>" + $(".student_name[num=" + ids[0] + "]").text() + " has been unstarred.</p>");
	                        } else {
	                    	    $("#message_area").html("<p>" + ids.length + " students unstarred.</p>");
	                        }
	                        break;
	                    case false:
	                    default:
	                        show_error_dialog(page_error_message);
	                        break;
	                };
	            },
	            error: function(jqXHR, textStatus, errorThrown) {
	                switch(jqXHR.status) {
	                    case 0:
	                        show_error_dialog(page_check_connection_message);
	                        break;
	                    default:
	                        show_error_dialog(page_error_message);
	                }
	            },
	        });
        } else {
        	$("#message_area").html(no_students_selected_message);
        }
    };

    function handle_star_student_toggle_click(e) {
        var container = this;
        var student_id = $(this).attr('num');
        $.ajax({
            type: 'POST',
            url: "/employer/star/student/toggle/",
            dataType: "json",
            data: {
                'student_id': student_id
            },
            beforeSend: function (jqXHR, settings) {
                place_tiny_ajax_loader(container);
            },
            success: function (data) {
                switch(data.valid) {
                    case true:
                        switch(data.action) {
                            case STARRED:
                           		$("#message_area").html("<p>" + $(".student_name[num=" + student_id + "]").text() + " has been starred.</p>");
                                $(container).html(STARRED_IMG);
                                break;
                            case UNSTARRED:
                           		$("#message_area").html("<p>" + $(".student_name[num=" + student_id + "]").text() + " has been unstarred.</p>");
                                $(container).html(UNSTARRED_IMG);
                                break;
                            default:
                                show_error_dialog(page_error_message);
                                break;
                        };
                        break;
                    case false:
                    default:
                        show_error_dialog(page_error_message);
                        break;
                };
            },
            error: function(jqXHR, textStatus, errorThrown) {
                switch(jqXHR.status) {
                    case 0:
                        show_error_dialog(page_check_connection_message);
                        break;
                    default:
                        show_error_dialog(page_error_message);
                }
            },
        });

    };

    function handle_resume_book_students_remove_click(e) {
        ids = []
        $(".student_checkbox").each( function(el) {
            if (this.checked)
                ids.push($(this).attr('num'));
        });
        if(ids.length){   
	        $.ajax({
	            type: 'POST',
	            url: "/employer/resume-book/students/remove/",
	            dataType: "json",
	            data: {
	                'student_ids': ids.join('~'),
	            },
	            beforeSend: function (jqXHR, settings) {
	                $(ids).each( function() {
	                    place_tiny_ajax_loader(".student_toggle_resume_book_link[num=" + this + "]");
	                });
	            },
	            success: function (data) {
	                initiate_resume_book_summary_update();
	                switch(data.valid) {
	                    case true:
	                        $(ids).each( function() {
	                            $(".student_toggle_resume_book_link[num=" + this + "]").html(ADD_TO_RESUME_BOOK_IMG);
	                            if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
									$(".student_main_info[num=" + this + "]").css({'opacity': ".7", 'background':'#FAFAFA'});
                                }
	                        });
	                        if (ids.length == 1){
                            	$("#message_area").html("<p>" + $(".student_name[num=" + ids[0] + "]").text() + " removed from resume book.</p>");
	                        } else {
	                    	    $("#message_area").html("<p>" + ids.length + " students removed from resume book.</p>");
	                        }
	                        break;
	                    case false:
	                    default:
	                        show_error_dialog(page_error_message);
	                        break;
	                };
	            },
	            error: function(jqXHR, textStatus, errorThrown) {
	                switch(jqXHR.status) {
	                    case 0:
	                        show_error_dialog(page_check_connection_message);
	                        break;
	                    default:
	                        show_error_dialog(page_error_message);
	                }
	            },
	        });
        } else {
        	$("#message_area").html(no_students_selected_message);
        }
    };

    function handle_resume_book_students_add_click(e) {
        ids = []
        $(".student_checkbox").each( function(el) {
            if (this.checked)
                ids.push($(this).attr('num'));
        });
        if(ids.length){            
            $.ajax({
                type: 'POST',
                url: "/employer/resume-book/students/add/",
                dataType: "json",
                data: {
                    'student_ids': ids.join('~'),
                },
                beforeSend: function (jqXHR, settings) {
                    $(ids).each( function() {
                        place_tiny_ajax_loader(".student_toggle_resume_book_link[num=" + this + "]");
                    });
                },
                success: function (data) {
                    initiate_resume_book_summary_update();
                    switch(data.valid) {
                        case true:
                            $(ids).each( function() {
                                $(".student_toggle_resume_book_link[num=" + this + "]").html(REMOVE_FROM_RESUME_BOOK_IMG);
                                if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
									$(".student_main_info[num=" + this + "]").css({'opacity': "1", 'background':'#FFF'});
                                }
                            });
                            if (ids.length == 1){
                            	$("#message_area").html("<p>" + $(".student_name[num=" + ids[0] + "]").text() + " added to resume book.</p>");
	                        } else {
	                    	    $("#message_area").html("<p>" + ids.length + " students added to resume book.</p>");
	                        }
                            break;
                        case false:
                        default:
                            show_error_dialog(page_error_message);
                            break;
                    };
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    switch(jqXHR.status) {
                        case 0:
                            show_error_dialog(page_check_connection_message);
                            break;
                        default:
                            show_error_dialog(page_error_message);
                    }
                },
            });
        } else {
        	$("#message_area").html(no_students_selected_message);
        }
    };

    function handle_student_toggle_resume_book_link_click(e) {
        var container = this;
        var student_id = $(this).attr('num');
        $.ajax({
            type: 'POST',
            url: '/employer/resume-book/student/toggle/',
            dataType: "json",
            beforeSend: function (arr, $form, options) {
                place_tiny_ajax_loader(container);
            },
            data: {
                'student_id': student_id,
            },
            success: function (data) {
                initiate_resume_book_summary_update();
                switch(data.valid) {
                    case true:
                        switch(data.action) {
                            case ADDED:
		                    	$("#message_area").html("<p>" + $(".student_name[num=" + student_id + "]").text() + " added to resume book.</p>");
                                if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
									$(".student_main_info[num=" + student_id + "]").css({'opacity': "1", 'background':'#FFF'});
                                }
                                $(container).html(REMOVE_FROM_RESUME_BOOK_IMG);
                                break;
                            case REMOVED:
		                    	$("#message_area").html("<p>" + $(".student_name[num=" + student_id + "]").text() + " removed from resume book.</p>");
                                if ($("#id_student_list").multiselect("getChecked")[0].title == IN_RESUME_BOOK_STUDENT_LIST) {
									$(".student_main_info[num=" + student_id + "]").css({'opacity': ".7", 'background':'#FAFAFA'});
                                }
                                $(container).html(ADD_TO_RESUME_BOOK_IMG);
                                break;
                            default:
                                show_error_dialog(page_error_message);
                                break;
                        };
                        break;
                    case false:
                    default:
                        show_error_dialog(page_error_message);
                        break;
                };
            },
            error: function(jqXHR, textStatus, errorThrown) {
                switch(jqXHR.status) {
                    case 0:
                        show_error_dialog(page_check_connection_message);
                        break;
                    default:
                        show_error_dialog(page_error_message);
                }
            },
        });
    };
    
    function save_student_comment(student_id, comment){
 		$.ajax({
            type: 'POST',
            url: '/employer/students/comment/',
            dataType: "json",
            data: {
                'student_id': student_id,
                'comment': comment,
            },
            success: function (data) {
            	$(".student_saved_note[num=" + student_id + "]").removeClass('hid');
            	window.setTimeout(function(){
            		$(".student_saved_note[num=" + student_id + "]").addClass('hid');
            	}, 3000);
                
                switch(data.valid) {
                    case true:
                        break;
                    case false:
                    default:
                        show_error_dialog(page_error_message);
                        break;
                };
            },
            error: function(jqXHR, textStatus, errorThrown) {
                switch(jqXHR.status) {
                    case 0:
                        show_error_dialog(page_check_connection_message);
                        break;
                    default:
                        show_error_dialog(page_error_message);
                }
            },
        });
    };
    
    function initiate_resume_book_summary_update() {
        $.ajax({
            type: 'POST',
            url: '/employer/resume-book/summary/',
            dataType: "html",
            beforeSend: function(arr, $form, options) {
                $("#num_of_students_in_resume_book_section #ajax_form_submit_loader").show();
            },
            complete: function(jqXHR, textStatus) {
                $("#num_of_students_in_resume_book_section #ajax_form_submit_loader").hide();
            },
            success: function (data) {
                $("#num_of_students_in_resume_book").html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                switch(jqXHR.status) {
                    case 0:
                        show_error_dialog(page_check_connection_message);
                        break;
                    default:
                        show_error_dialog(page_error_message);
                }
            },
        });
    };

    function handle_student_hide_details_link_click() {
        var id = $(this).attr('num');
        $('.student_detailed_info[num=' + id  + ']').slideUp('slow');
        $('.student_toggle_detailed_info_link[num=' + id  + ']').html(SHOW_DETAILS_LINK);
    };
    
    function handle_student_toggle_detailed_info_link_click() {
        var id = $(this).attr('num');
        if ($(this).children('span').attr('class') === "hide_details") {
            $('.student_detailed_info[num=' + id  + ']').slideUp('slow');
            $(this).html(SHOW_DETAILS_LINK);
        } else {
            $('.student_detailed_info[num=' + id  + ']').slideDown('slow');
            $(this).html(HIDE_DETAILS_LINK);
        }
    };
    
    function handle_results_menu_toggle_details_button_click() {
        if( $("#results_menu_toggle_details span").html()=="Show All Details") {
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
    	$(".starred_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', true);
    	});
    	$(".unstarred_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', false);
    	});
    };

    function handle_results_menu_not_starred_click(e) {
    	$(".starred_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', false);
    	});
    	$(".unstarred_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', true);
    	});
    };

    function handle_results_menu_in_resume_book_click(e) {
    	$(".add_to_resume_book_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', false);
    	});
    	$(".remove_from_resume_book_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', true);
    	});
    };

    function handle_results_menu_not_in_resume_book_click(e) {
    	$(".add_to_resume_book_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', true);
    	});
    	$(".remove_from_resume_book_img").each(function() {
    		var num = $(this).parent('a').attr('num');
    		$(".student_checkbox[num=" + num  + "]").attr('checked', false);
    	});
    };
            
    function handle_results_menu_checkbox_click(e){
        if($("#results_menu_checkbox").attr('checked')==false) {
            $(".student_checkbox:checked").each( function() {
                $(this).attr('checked', false);
            });
        } else {
            $(".student_checkbox").not(':checked').each( function() {
                $(this).attr('checked', true);
            });
        }
        e.stopPropagation();
    };
    
    function handle_menu_all_on_page_click(){
        $(".student_checkbox").not(':checked').each( function() {
            $(this).attr('checked', true);
        });
    };
    
    function handle_multiselect_open_in_accordion(event, ui) {
    	/*
        var parent = $(event.target).parents(".ui-accordion-content");
        var multiselect = $(event.target).multiselect('widget');
        var new_height = multiselect.height() + parseInt(multiselect.css('top'), 10);
        $(parent).css('height', new_height);
        */
    };

    function handle_multiselect_close_in_accordion(event, ui) {
    	/*
        $('#' + $(event.target).attr('id')).parents(".ui-accordion-content").css("height", "");
        */
    };

    function campus_org_link_click_handler() {
    	campus_org_id = $(this).attr('num');
        campus_org_info_dialog = open_campus_org_info_dialog($(this).text());
        campus_org_info_dialog.html(dialog_ajax_loader);

        var campus_org_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, 10000);
        $.ajax({
            type: 'GET',
            url: '/get-campus-org-info/',
            dataType: "html",
            data: {
                'campus_org_id': campus_org_id,
            },
            success: function (data) {
                clearTimeout(campus_org_info_dialog_timeout);
                campus_org_info_dialog.html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(campus_org_info_dialog_timeout);
                switch(jqXHR.status) {
                    case 0:
                        campus_org_info_dialog.html(dialog_check_connection_message);
                        break;
                    default:
                        campus_org_info_dialog.html(dialog_error_message);
                }
            },
        });
    };
	
	function handle_event_invitation_link_click() {
		open_event_invitation_dialog();
	};
	
    function course_link_click_handler() {
    	var course_id = $(this).attr('num');
        course_info_dialog = open_course_info_dialog($(this).text());
        course_info_dialog.html(dialog_ajax_loader);

        var course_info_dialog_timeout = setTimeout(show_long_load_message_in_dialog, 10000);
        $.ajax({
            type: 'GET',
            url: '/get-course-info/',
            dataType: "html",
            data: {
                'course_id': course_id,
            },
            success: function (data) {
                clearTimeout(course_info_dialog_timeout);
                course_info_dialog.html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(course_info_dialog_timeout);
                switch(jqXHR.status) {
                    case 0:
                        course_info_dialog.html(dialog_check_connection_message);
                        break;
                    default:
                        course_info_dialog.html(dialog_error_message);
                }
            },
        });
    };

    function handle_page_link_click() {
        page = $(this).attr("id").substring(5);
        initiate_ajax_call();
    };
    
    function initiate_search() {
        query = $("#query_field").val().replace(/[^a-z\d ]+/ig,'');
        initiate_ajax_call();
    };
	
    function initiate_ajax_call() {
    	var xhr;
    	if(xhr && xhr.readystate != 4){ xhr.abort(); }
    	$("#message_area").html("");
        $("#results_block_content").css('opacity', 0.25);
        $("#results_block_info_section").css('display', 'block');
        $("#results_block_info").html(long_horizontal_ajax_loader);
        var error_dialog_timeout = setTimeout( function() {
            $("#results_block_info").prepend(two_line_long_load_message);
        }, 10000);
	
        xhr = $.ajax({
            type: 'POST',
            url: '/employer/students/',
            dataType: "html",
            data: {
                'page': page,
                'student_list': student_list,
                'query': query,
                'gpa' : min_gpa,
                'act': min_act,
                'sat_t' : min_sat_t,
                'sat_m' : min_sat_m,
                'sat_v' : min_sat_v,
                'sat_w' : min_sat_w,
                'courses' : courses.join('~'),
                'school_years' : school_years.join('~'),
                'graduation_years' : graduation_years.join('~'),
                'employment_types' : employment_types.join('~'),
                'previous_employers' : previous_employers.join('~'),
                'industries_of_interest' : industries_of_interest.join('~'),
                'campus_orgs' : campus_orgs.join('~'),
                'languages' : languages.join('~'),
                'countries_of_citizenship' : countries_of_citizenship.join('~'),
                'older_than_18' : older_than_18,
                'ordering': ordering,
                'results_per_page': results_per_page,
            },
            success: function (data) {
                clearTimeout(error_dialog_timeout);
                $('#results_block_content').html(data);
				
				$(".student_comment").autoResize({
				    animateDuration : 0,
				    extraSpace : 18
				});
                // Results Menu Styles
                $('.dropdown_menu_button ul').hide();

                // Hide all extra details except for the first
                $(".student_detailed_info").hide();
                $('.student_detailed_info[num=0]').show();
                $('.student_toggle_detailed_info_link[num=0]').html(HIDE_DETAILS_LINK);

                // Bring the opacity back to normal and hide the ajax loader
                $("#results_block_content").css('opacity', 1);
                $("#results_block_info_section").css('display', 'none');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(error_dialog_timeout);
                switch(jqXHR.status) {
                    case 0:
                        $("#results_block_info").html(check_connection_message + " by clicking <a id='initiate_ajax_call' class='error' href='javascript:void(0)'>here</a>.</p>");
                        break;
                    default:
                        $("#results_block_info").html(page_error_message);
                }
            },
        });
    };
    function handle_deliver_resume_book_button_click() {
        deliver_resume_book_dialog = open_deliver_resume_book_dialog();
        deliver_resume_book_dialog.html(dialog_ajax_loader);

        var resume_book_created = false;

        var deliver_resume_book_dialog_timeout = setTimeout(show_long_load_message_in_dialog, 10000);
        $.ajax({
            dataType: "html",
            url: '/employer/resume-books/deliver/',
            error: function(jqXHR, textStatus, errorThrown) {
                clearTimeout(deliver_resume_book_dialog_timeout);
                switch(jqXHR.status) {
                    case 0:
                        deliver_resume_book_dialog.html(dialog_check_connection_message);
                        break;
                    default:
                        deliver_resume_book_dialog.html(dialog_error_message);
                }
            },
            success: function (data) {
                clearTimeout(deliver_resume_book_dialog_timeout);

                deliver_resume_book_dialog.html(data);
                deliver_resume_book_dialog.dialog('option', 'position', 'center');

                $("label[for=id_email]").addClass('required');

                $("#id_delivery_type").multiselect({
                    noneSelectedText: "select delivery type",
                    height:53,
                    header:false,
                    show: multiselectShowAnimation,
                    hide: multiselectHideAnimation,
                    minWidth:multiselectSingleSelectWidth,
                    selectedList: 1,
                    multiple: false,
                    click: function(event, ui) {
                        if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                            $('.email_delivery_type_only_field').show()
                            $('#id_email').rules("add", {
                                email: true,
                                required: true
                            });
                            $("#deliver_resume_book_form_submit_button").val("Email");
                        } else {
                            $('.email_delivery_type_only_field').hide();
                            $('#id_email').rules("remove", "email required");
                            $("#deliver_resume_book_form_submit_button").val("Download");
                        }
                    }
                });

                var deliver_resume_book_form_validator = $("#deliver_resume_book_form").validate({
                    submitHandler: function(form) {
                        if (resume_book_created) {
                            var custom_resume_book_name = $("#id_name").val();
                            if($("#id_delivery_type").multiselect("getChecked")[0].value === EMAIL_DELIVERY_TYPE) {
                                $(form).ajaxSubmit({
                                    data : {
                                        'name' : custom_resume_book_name
                                    },
                                    dataType: 'json',
                                    beforeSubmit: function (arr, $form, options) {
                                        show_form_submit_loader("#deliver_resume_book_form");
                                    },
                                    error: function(jqXHR, textStatus, errorThrown) {
                                        hide_form_submit_loader("#deliver_resume_book_form");
                                        switch(jqXHR.status) {
                                            case 0:
                                                deliver_resume_book_dialog.html(dialog_check_connection_message);
                                                break;
                                            default:
                                                deliver_resume_book_dialog.html(dialog_error_message);
                                        }
                                    },
                                    success: function(data) {
                                        hide_form_submit_loader("#deliver_resume_book_form");
                                        switch(data.valid) {
                                            case true:
                                                deliver_resume_book_dialog.html(resume_book_delivered_message);
                                                break;
                                            case false:
                                                deliver_resume_book_dialog.html(dialog_error_message);
                                                break;
                                            default:
                                                deliver_resume_book_dialog.html(dialog_error_message);
                                                break;
                                        }
                                        deliver_resume_book_dialog.dialog('option', 'position', 'center');
                                    }
                                });
                            } else {
                                var download_url = "/employer/resume-books/download/"
                                if (custom_resume_book_name){
                                    download_url = download_url + "?name=" + escape(custom_resume_book_name)
                                }
                                window.location.href = download_url;
                                deliver_resume_book_dialog.html(resume_book_delivered_message);
                            }
                            deliver_resume_book_dialog.dialog('option', 'title', 'Resume Book Successfully Delivered');
                        } else {
                            $("#deliver_resume_book_form .error_section").html("Please wait until the resume book is ready.");
                        }
                    },
                    highlight: highlight,
                    unhighlight: unhighlight,
                    errorPlacement: place_errors_table,
                    rules: {
                        email: {
                            email: true,
                        },
                        delivery_type: {
                            required: true
                        },
                    },
                });

                $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: '/employer/resume-books/create/',
                    error: function(jqXHR, textStatus, errorThrown) {
                        switch(jqXHR.status) {
                            case 0:
                                deliver_resume_book_dialog.html(dialog_check_connection_message);
                                break;
                            default:
                                deliver_resume_book_dialog.html(dialog_error_message);
                        }
                    },
                    success: function (data) {
                        resume_book_created = true;
                        $("#resume_book_status").html("Ready");
                        $("#resume_book_status").addClass('ready');
                        $("#resume_book_status").removeClass('warning');                        
                    }
                });
            }
        });
    };

    function set_up_side_block_scrolling() {
        var el = $('#side_block_area');
        var elpos_original = el.offset().top;
        $(window).scroll( function() {
            var elpos = el.offset().top;
            var windowpos = $(window).scrollTop();
            var finaldestination = windowpos;
            if(windowpos<elpos_original) {
                finaldestination = elpos_original;
                el.stop(true).animate({
                    'top' : 0
                }, 400, 'easeInOutExpo');
            } else {
                el.stop(true).animate({
                    'top' : windowpos-70
                }, 400, 'easeInOutExpo');
            }
        });
    };
    
    $("#id_student_list").multiselect({
        header:false,
        multiple: false,
        selectedList: 1,
        height:146,
        minWidth:multiselectMinWidth,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        click: function(event, ui) {
            student_list = ui.text;
            initiate_ajax_call();
        }
    });

    $("#id_majors").multiselect({
        noneSelectedText: 'Filter By Major',
        selectedText: 'Filtering by # Majors',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            courses = $("#id_majors").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            courses = $("#id_majors").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            courses = $("#id_majors").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_school_years").multiselect({
        noneSelectedText: 'Filter By School Year',
        selectedText: 'Filtering by # School Years',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 97,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            school_years = $("#id_school_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            school_years = $("#id_school_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            school_years = $("#id_school_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    });

    $("#id_graduation_years").multiselect({
        noneSelectedText: 'Filter By Graduation Year',
        selectedText: 'Filtering by # Graduation Years',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 97,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            graduation_years = $("#id_graduation_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            graduation_years = $("#id_graduation_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            graduation_years = $("#id_graduation_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    });

    $("#id_employment_types").multiselect({
        noneSelectedText: 'Filter By Employment Type',
        selectedText: 'Filtering by # Employment Types',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 97,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            employment_types = $("#id_employment_types").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            employment_types = $("#id_employment_types").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            employment_types = $("#id_employment_types").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    });

    $("#id_previous_employers").multiselect({
        noneSelectedText: 'Filter By Previous Employers',
        selectedText: 'Filtering by # Previous Employers',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            previous_employers = $("#id_previous_employers").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            previous_employers = $("#id_previous_employers").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            previous_employers = $("#id_previous_employers").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_industries_of_interest").multiselect({
        noneSelectedText: 'Filter By Industries of Interest',
        selectedText: 'Filtering by # Industries of Interest',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            industries_of_interest = $("#id_industries_of_interest").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            industries_of_interest = $("#id_industries_of_interest").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            industries_of_interest = $("#id_industries_of_interest").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_campus_involvement").multiselect({
        noneSelectedText: 'Filter By Campus Involvement',
        selectedText: 'Filtering by # Campus Organizations',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        optgrouptoggle: function(e, ui) {
            /* To do */
        },
        checkAll: function() {
            campus_orgs = $("#id_campus_involvement").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            campus_orgs = $("#id_campus_involvement").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            campus_orgs = $("#id_campus_orgs").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_languages").multiselect({
        noneSelectedText: 'Filter By Languages',
        selectedText: 'Filtering by # Languages',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            languages = $("#id_languages").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            languages = $("#id_languages").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            languages = $("#id_languages").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_countries_of_citizenship").multiselect({
        noneSelectedText: 'Filter By Country',
        selectedText: 'Filtering by # Countries',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        minWidth:multiselectMinWidth,
        height: 146,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        checkAll: function() {
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();

    $("#id_older_than_18").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        height: 47,
        minWidth: multiselectYesNoSingleSelectWidth,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        click: function(event, ui) {
            older_than_18 = ui.value;
            initiate_ajax_call();
        }
    });

    $("#id_ordering").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        height: 97,
        minWidth:multiselectSingleSelectWidth,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        click: function(event, ui) {
            ordering = ui.value;
            initiate_ajax_call();
        }
    });

    $("#id_results_per_page").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        show: multiselectShowAnimation,
        hide: multiselectHideAnimation,
        height: 97,
        minWidth:multiselectSingleSelectWidth,
        open: handle_multiselect_open_in_accordion,
        close: handle_multiselect_close_in_accordion,
        click: function(event, ui) {
            results_per_page = ui.value;
            initiate_ajax_call();
        }
    });

    // GPA Slider
    $("#gpa_filter_section div").slider({
        min: 0,
        max: 5.0,
        step: .1,
        value: 0.0,
        slide: function(event, ui) {
            $("#id_gpa").val(formatNumber(ui.value, 1,' ','.','','','-','').toString());
        },
        change: function(event, ui) {
            if (min_gpa != ui.value) {
                page = 1;
                min_gpa = ui.value;
                initiate_ajax_call();
            }
        }
    });

    // SAT Total Slider
    $("#sat_t_filter_section div").slider({
        min: 600,
        max: 2400,
        step: 10,
        value: 600,
        slide: function(event, ui) {
            $("#id_sat_t").val(ui.value);
        },
        change: function(event, ui) {
            if (min_sat_t != ui.value) {
                page = 1;
                min_sat_t = ui.value;
                initiate_ajax_call();
            }
        }
    });


    // SAT Math Slider
    $("#sat_m_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#id_sat_m").val(ui.value);
        },
        change: function(event, ui) {
            if (min_sat_m != ui.value) {
                page = 1;
                min_sat_m = ui.value;
                initiate_ajax_call();
            }
        }
    });

    // SAT Verbal Slider
    $("#sat_v_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#id_sat_v").val(ui.value);
        },
        change: function(event, ui) {
            if (min_sat_v != ui.value) {
                page = 1;
                min_sat_v = ui.value;
                initiate_ajax_call();
            }
        }
    });

    // SAT Writing Slider
    $("#sat_w_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#id_sat_w").val(ui.value);
        },
        change: function(event, ui) {
            if (min_sat_w != ui.value) {
                page = 1;
                min_sat_w = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //ACT Slider
    $("#act_filter_section div").slider({
        min: 0,
        max: 36,
        step: 1,
        value: 0,
        slide: function(event, ui) {
            $("#id_act").val(ui.value);
        },
        change: function(event, ui) {
            if (min_act != ui.value) {
                page = 1;
                min_act = ui.value;
                initiate_ajax_call();
            }
        }
    });
    
    $("#id_gpa").val($("#gpa_filter_section div").slider("value"));
    $("#id_act").val($("#act_filter_section div").slider("value"));
    $("#id_sat_t").val($("#sat_t_filter_section div").slider("value"));
    $("#id_sat_m").val($("#sat_m_filter_section div").slider("value"));
    $("#id_sat_v").val($("#sat_v_filter_section div").slider("value"));
    $("#id_sat_w").val($("#sat_w_filter_section div").slider("value"));
    
    $(".event_invitation_link").live('click', handle_event_invitation_link_click);
    $("#results_menu_in_resume_book").live('click', handle_results_menu_in_resume_book_click);
    $("#results_menu_not_in_resume_book").live('click', handle_results_menu_not_in_resume_book_click);
    $("#results_menu_not_starred").live('click', handle_results_menu_not_starred_click);
    $("#results_menu_starred").live('click', handle_results_menu_starred_click);
	$("#results_menu_all_on_page").live('click', handle_menu_all_on_page_click);
    $("#results_menu_checkbox").live('click', handle_results_menu_checkbox_click);
    $(".campus_org_link").live('click', campus_org_link_click_handler);
    $(".course_link").live('click', course_link_click_handler);
	$("#switch_to_students_in_resume_book_student_list_link").live('click', switch_to_students_in_resume_book_student_list);
	$("#switch_to_students_in_resume_book_student_list_dialog_link").live('click', switch_to_students_in_resume_book_student_list_dialog );
    $(".student_toggle_resume_book_link").live('click', handle_student_toggle_resume_book_link_click);
    $(".student_toggle_star_link").live('click', handle_star_student_toggle_click);
    $("#star_students_add").live('click', handle_star_students_add_click);
    $("#star_students_remove").live('click', handle_star_students_remove_click);
    $("#resume_book_students_add").live('click', handle_resume_book_students_add_click);
    $("#resume_book_students_remove").live('click', handle_resume_book_students_remove_click);
    $("#results_menu_toggle_details").live('click', handle_results_menu_toggle_details_button_click );
    $(".student_toggle_detailed_info_link").live('click', handle_student_toggle_detailed_info_link_click);
    $(window).resize(set_up_side_block_scrolling);
    $(".student_hide_details_link").live('click', handle_student_hide_details_link_click);
    $("#search_form_submit_button").click(initiate_search);
    $(".page_link").live('click', handle_page_link_click);
    $('#student_deliver_resume_book_button').click(handle_deliver_resume_book_button_click);
    $("#initiate_ajax_call").live('click', initiate_ajax_call);
	$(".student_comment").live('blur', function(){ $(this).height(17); }); 
    $('#results_menu_more_actions').live('click', function() { $('#results_menu_more_actions ul').toggle(); });
    $('#results_menu_checkbox_menu_button').live('click', function() { $('#results_menu_checkbox_menu_button ul').toggle(); });
    
    $('.dropdown_menu_button').live('click', function() {
        if ($(this).hasClass('pressed'))
            $(this).removeClass('pressed');
        else
            $(this).addClass('pressed');
    });
    $('body').live('click', function(event) {
        if (!$(event.target).closest('.dropdown_menu_button').length && !$(event.target).closest('.dropdown menu_button ul').length) {
            $('.dropdown_menu_button ul').hide();
            $('.dropdown_menu_button').removeClass('pressed');
        };
    });

    // Make the filtering block an accordion
    a = $("#filtering_accordion").accordion({
        autoHeight: false,
        clearStyle: true,
        collapsible: true
    });

    $("#query_field").val(query);
    var timeoutID;
    $('#query_field').keydown( function() {
        if (typeof timeoutID!='undefined')
            window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(initiate_search, 1000);
    });
    
	$('.student_comment').live('keydown', function() {
		var student_id = $(this).attr('num');
		var textarea = this;
        if (typeof timeoutID!='undefined')
            window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout( function(){
        	save_student_comment(student_id, $(textarea).val());
        }, 1000);
    });

    set_up_side_block_scrolling();
    initiate_ajax_call();
    initiate_resume_book_summary_update();
});