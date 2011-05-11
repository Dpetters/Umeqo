/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
	
	/* Filtering Variables */
	var min_gpa = 0;
	var min_act = 0;
	var min_sat_t = 600;
	var min_sat_m = 200;
	var min_sat_v = 200;
	var min_sat_w = 200;
	var page = 1;
	var student_list = $("#id_student_list option:selected").val(); 
	var ordering = $("#id_ordering option:selected").val();
	var results_per_page = $("#id_results_per_page option:selected").val();
	var courses = new Array();
	var school_years = new Array();
	var graduation_years = new Array();
	var previous_employers = new Array();
	var industries_of_interest = new Array();
	var looking_for_internship = null;
	var looking_for_fulltime = null;
	var languages = new Array();
	var campus_organizations = new Array()
	var must_be_older_than_18 = false;

	function handle_multiselect_open_in_accordion(event, ui) {
		var parent = $(event.target).parents(".ui-accordion-content");
		var multiselect = $(event.target).multiselect('widget');
		var new_height = multiselect.height() + parseInt(multiselect.css('top'), 10);
		$(parent).css('height', new_height);
	};
	
	function handle_multiselect_close_in_accordion(event, ui) {
			$('#' + $(event.target).attr('id')).parents(".ui-accordion-content").css("height", "");
	};

	function campus_org_link_click() {
		alert("Campus org link click func not implemented!")
	};
	
	function initiate_search() {
		query = $("#query_field").val().replace(/[^a-z\d ]+/ig,'');
		initiate_ajax_call();
	};
	
	$("#initiate_ajax_call").live('click', initiate_ajax_call);

	function initiate_ajax_call() {
		$("#results_section").css('opacity', 0.3);
		$("#results_block_info_section").css('display', 'block');
		$("#results_block_info").html(ajax_loader);
		var error_dialog_timeout = setTimeout(function(){$(long_load_message).insert("#results_block_info img");}, 10000);
		$.ajax({
			type: 'POST',
			url: '/employer/student-filtering/',
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
				'courses' : courses,
				'ordering': ordering,
				'results_per_page': results_per_page,
			},
			success: function (data) {
				clearTimeout(error_dialog_timeout);
				$('#results_section').html(data);

				// Hide all extra details except for the first
				$(".student_detailed_info").hide();
				$("#student_detailed_info_0").show();
				$(".view_student_detailed_info_link_cell #0").text("Hide Details");

				$(".student_drag_anchor").draggable({
					'revert':true,
					helper: function(event) {
						return $("<div class='student_drag_div'>" + $(this).parent(".student_checkbox_cell").next().find(".student_name").text() + "</div>");
					},
					'revertDuration': 100,
					'drag': function(event, ui) {
						$("#resume_book_block .side_block_content").html("<p>Drop student's name here!</p>");
					}
				});

				// Bring the opacity back to normal and hide the ajax loader
				$("#results_section").css('opacity', 1);
				$("#results_block_info_section").css('display', 'none');
			},
            error: function(jqXHR, textStatus, errorThrown) {
				clearTimeout(error_dialog_timeout);
                switch(jqXHR.status){
                    case 0:
                    	$("#results_block_info").html(check_connection_message + " by clicking <a id='initiate_ajax_call' class='error' href='javascript:void(0)'>here</a>.</p>");
                        break;
                    default:
                    	$("#results_block_info").html(page_error_message);
                }
            },
		});
	};
	
	// Listen for a campus organization info link click
	$(".campus_org_link").live('click', campus_org_link_click);
	
	// Listen for a new search
	$("#search_form_submit_button").click(initiate_search);

	// Listen for results per page change
	$("#id_results_per_page").change( function() {
		results_per_page = $("#id_results_per_page option:selected").val();
		initiate_ajax_call();
	});
	
	// Listen for result ordering change
	$("#id_ordering").change( function() {
		ordering = $("#id_ordering option:selected").val();
		initiate_ajax_call();
	});
	
	// Listen for result page change
	$(".page_link").live('click', function() {
		page = $(this).attr("id").substring(5);
		initiate_ajax_call();
	});

	// Listen for result detailed info toggle
	$(".view_student_detailed_info_link").live('click', function() {
		var selector = ".view_student_detailed_info_link_cell #" + this.id;

		if ($(selector).text() === "Hide Details")
			$(selector).text("View Details");
		else
			$(selector).text("Hide Details");
		$('#student_detailed_info_'+ this.id).slideToggle('slow');
	});

	// Listen for mater checkbox click
	$("#results_menu_checkbox").live('click', function() {
		if($("#results_menu_checkbox").attr('checked')==false) {
			$(".student_checkbox:checked").each( function() {
				$(this).attr('checked', false);
			});
		} else {
			$(".student_checkbox").not(':checked').each( function() {
				$(this).attr('checked', true);
			});
		}
	});
	// Listen for hide/view all details click
	$("#results_menu_toggle_details").live('click', function() {
		if( $("#results_menu_toggle_details span").text()=="View All Details") {
			$(".view_student_detailed_info_link").text("Hide Details");
			$(".student_detailed_info").show('slow');
			$("#results_menu_toggle_details span").text("Hide All Details");
		} else {
			$(".view_student_detailed_info_link").text("Show Details");
			$(".student_detailed_info").hide('slow');
			$("#results_menu_toggle_details span").text("View All Details");
		}
	});
	
	
	$("#id_student_list").multiselect({
		header:false,
		multiple: false,
		selectedList: 1,
		height:multiselectLargeHeight,
		minWidth:multiselectMinWidth,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		click: function(event, ui){
			student_list = ui.value;
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
		height: multiselectLargeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_school_years").multiselect({
		noneSelectedText: 'Filter By School Year',
		selectedText: 'Filtering by # School Years',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectMediumHeight,
		//open: handle_multiselect_open_in_accordion,
		//close: handle_multiselect_close_in_accordion
	});

	$("#id_graduation_years").multiselect({
		noneSelectedText: 'Filter By Graduation Year',
		selectedText: 'Filtering by # Graduation Years',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectMediumHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_employment_types").multiselect({
		noneSelectedText: 'Filter By Employment Type',
		selectedText: 'Filtering by # Employment Types',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectTwoOptionHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});
	
	$("#id_previous_employers").multiselect({
		noneSelectedText: 'Filter By Previous Employers',
		selectedText: 'Filtering by # Previous Employers',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectLargeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_industries_of_interest").multiselect({
		noneSelectedText: 'Filter By Industries of Interest',
		selectedText: 'Filtering by # Industries of Interest',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectLargeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_languages").multiselect({
		noneSelectedText: 'Filter By Languages',
		selectedText: 'Filtering by # Languages',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectLargeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();


	$("#id_campus_orgs").multiselect({
		noneSelectedText: 'Filter By Campus Involvement',
		selectedText: 'Filtering by # Campus Organizations',
		checkAllText: multiselectCheckAllText,
		uncheckAllText: multiselectUncheckAllText,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		minWidth:multiselectMinWidth,
		height: multiselectLargeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_older_than_18").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		height: multiselectTwoOptionHeight,
		minWidth: multiselectYesNoSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_citizen").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		height: multiselectTwoOptionHeight,
		minWidth:multiselectYesNoSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});
	
	$("#id_ordering").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		height: multiselectTwoOptionHeight,
		minWidth:multiselectSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_results_per_page").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: multiselectShowAnimation,
		hide: multiselectHideAnimation,
		height: multiselectTwoOptionHeight,
		minWidth:multiselectSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion,
		click: function(event, ui){
			results_per_page = ui.value;
			initiate_ajax_call();
		}
	});

	// GPA Slider
	$("#gpa_filter_section div").slider({
		min: 0,
		max: 5.0,
		step: .1,
		value: 0,
		slide: function(event, ui) {
			$("#id_gpa").val(ui.value);
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
	
	// Make the resume block into a droppable area
	$("#resume_book_block .side_block_content").droppable({
		activeClass: "add_to_resume_book_area_active",
		hoverClass: "add_to_resume_book_area_hover",
		drop: function(event, ui) {
			$.ajax({
				'url':'/employer/add-to-resume-book/' + $(ui.draggable).attr("id").substring(4) + "/",
				success: function(date) {
				}
			});
		}
	});
		
	// Set up side block area scrolling
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
				'top' : windowpos-80
			}, 400, 'easeInOutExpo');
		}
	});
	
	// Make the filtering block an accordion
	a = $("#filtering_accordion").accordion({
		autoHeight: false,
		clearStyle: true,
		collapsible: true
	});


	// Make the first ajax call for results automatically
	initiate_ajax_call();
});
