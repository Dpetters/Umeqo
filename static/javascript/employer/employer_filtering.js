/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	/* FILTERING VARIABLES */
	var min_gpa = 0;
	var min_act = 0;
	var min_sat = 600;
	var page = 1;
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

	// Listen for a campus organization info
	$(".campus_org_link").live('click', campus_org_link_click);

	var initiate_search = function() {
		query = $("#query_field").val().replace(/[^a-z\d ]+/ig,'');
		initiate_ajax_call();
	};
	
	// Listen for a new search
	$("#search_form_submit_button").live('click', initiate_search);

	// Listen for Results per page sections
	$("#id_results_per_page").change( function() {
		results_per_page = $("#id_results_per_page option:selected").val();
		initiate_ajax_call();
	});
	// Listen for Ordering Changes
	$("#id_ordering").change( function() {
		ordering = $("#id_ordering option:selected").val();
		initiate_ajax_call();
	});
	// Listen for page changes
	$(".page_link").live('click', function() {
		page = $(this).attr("id").substring(5);
		initiate_ajax_call();
	});
	$("#id_student_list").multiselect({
		height:138,
		header:false,
		minWidth:318,
		selectedList: 1,
		multiple: false
	});

	$("#id_majors").multiselect({
		noneSelectedText: 'Filter By Major',
		selectedText: 'Filtering by # Majors',
		checkAllText: "All",
		minWidth:318,
		height: 120,
		uncheckAllText: "None",
		close: function(e) {
			$("#id_majors").parents(".ui-accordion-content").css("height", "");
		},
	}).multiselectfilter();

	$("#id_school_years").multiselect({
		noneSelectedText: 'Filter By School Year',
		selectedText: 'Filtering by # School Years',
		checkAllText: "All",
		minWidth:318,
		height: 86,
		uncheckAllText: "None",
	});

	$("#id_graduation_years").multiselect({
		noneSelectedText: 'Filter By Graduation Year',
		selectedText: 'Filtering by # Graduation Years',
		checkAllText: "All",
		minWidth:318,
		height: 86,
		open: function(event, ui) {
			var parent = $("#id_graduation_years").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_graduation_years").nextAll(".ui-multiselect-menu").height()+125);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_graduation_years").parents(".ui-accordion-content").css("height", "");
		},
	});

	$("#id_employment_types").multiselect({
		noneSelectedText: 'Filter By Employment Type',
		selectedText: 'Filtering by # Employment Types',
		checkAllText: "All",
		minWidth:318,
		height: 50,
		open: function(event, ui) {
			var parent = $("#id_employment_types").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_employment_types").nextAll(".ui-multiselect-menu").height()+45);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_employment_types").parents(".ui-accordion-content").css("height", "");
		},
	});
	
	$("#id_previous_employers").multiselect({
		noneSelectedText: 'Filter By Previous Employers',
		selectedText: 'Filtering by # Previous Employers',
		checkAllText: "All",
		minWidth:318,
		height: 90,
		open: function(event, ui) {
			var parent = $("#id_previous_employers").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_previous_employers").nextAll(".ui-multiselect-menu").height()+75);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_previous_employers").parents(".ui-accordion-content").css("height", "");
		},
	}).multiselectfilter();

	$("#id_industries_of_interest").multiselect({
		noneSelectedText: 'Filter By Industries of Interest',
		selectedText: 'Filtering by # Industries of Interest',
		checkAllText: "All",
		minWidth:318,
		height: 110,
		open: function(event, ui) {
			var parent = $("#id_industries_of_interest").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_industries_of_interest").nextAll(".ui-multiselect-menu").height()+110);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_industries_of_interest").parents(".ui-accordion-content").css("height", "");
		},
	}).multiselectfilter();

	$("#id_languages").multiselect({
		noneSelectedText: 'Filter By Languages',
		selectedText: 'Filtering by # Languages',
		checkAllText: "All",
		minWidth:318,
		height: 120,
		open: function(event, ui) {
			var parent = $("#id_languages").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_languages").nextAll(".ui-multiselect-menu").height()+45);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_languages").parents(".ui-accordion-content").css("height", "");
		},
	}).multiselectfilter();


	$("#id_campus_orgs").multiselect({
		noneSelectedText: 'Filter By Campus Organizations',
		selectedText: 'Filtering by # Campus Organizations',
		checkAllText: "All",
		minWidth:318,
		height: 140,
		open: function(event, ui) {
			var parent = $("#id_campus_orgs").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_campus_orgs").nextAll(".ui-multiselect-menu").height()+75);
		},
		uncheckAllText: "None",
		close: function(e) {
			$("#id_campus_orgs").parents(".ui-accordion-content").css("height", "");
		},
	}).multiselectfilter();

	$("#id_older_than_18").multiselect({
		height:47,
		header:false,
		minWidth:182,
		selectedList: 1,
		multiple: false
	});

	$("#id_citizen").multiselect({
		height:47,
		header:false,
		minWidth:182,
		selectedList: 1,
		multiple: false,
		open: function(event, ui) {
			var parent = $("#id_citizen").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_citizen").nextAll(".ui-multiselect-menu").height()+150);
		},
		close: function(e) {
			$("#id_citizen").parents(".ui-accordion-content").css("height", "");
		},
	});
	
	$("#id_ordering").multiselect({
		height:47,
		header:false,
		minWidth:202,
		selectedList: 1,
		multiple: false
	});

	$("#id_results_per_page").multiselect({
		height:47,
		header:false,
		minWidth:202,
		selectedList: 1,
		multiple: false,
		open: function(event, ui) {
			var parent = $("#id_results_per_page").parents(".ui-accordion-content");
			$(parent).css('height', $("#id_results_per_page").nextAll(".ui-multiselect-menu").height()+85);
		},
		close: function(e) {
			$("#id_results_per_page").parents(".ui-accordion-content").css("height", "");
		},
	});

	// Result Collapse
	$(".view_student_detailed_info_link").live('click', function() {
		var selector = ".view_student_detailed_info_link_cell #" + this.id;

		if ($(selector).text() === "Hide Details")
			$(selector).text("View Details");
		else
			$(selector).text("Hide Details");
		$('#student_detailed_info_'+ this.id).slideToggle('slow');
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

	// SAT Slider
	$("#sat_filter_section div").slider({
		min: 600,
		max: 2400,
		step: 10,
		value: 600,
		slide: function(event, ui) {
			$("#id_sat").val(ui.value);
		},
		change: function(event, ui) {
			if (min_sat != ui.value) {
				page = 1;
				min_sat = ui.value;
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
	$("#id_sat").val($("#sat_filter_section div").slider("value"));

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

	function campus_org_link_click() {

	};


	var initiate_ajax_call = function() {
		$("#results_section").css('opacity', 0.5);
		$("#results_block_loader_section").css('display', 'block');

		$.ajax({
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
			},
			type: 'POST',
			url: '/employer/student-filtering/',
			dataType: "html",
			data: {
				'results_per_page':20,
				'query': query,
				'gpa' : min_gpa,
				'act': min_act,
				'sat' : min_sat,
				'page': page,
				'ordering': ordering,
				'results_per_page': results_per_page,
				'courses' : courses
			},
			success: function (data) {
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
				$("#results_block_loader_section").css('display', 'none');
			}
		});
	};
	// Handle the selection of all checkboxes
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
	// Hide/Show All Details Menu Button
	$("#results_menu_toggle_details").live('click', function() {
		if( $("#results_menu_toggle_details span").text()=="View All Details") {
			$(".view_student_detailed_info_link").text("Show Details");
			$(".student_detailed_info").show('slow');
			$("#results_menu_toggle_details span").text("Hide All Details");
		} else {
			$(".view_student_detailed_info_link").text("Hide Details");
			$(".student_detailed_info").hide('slow');
			$("#results_menu_toggle_details span").text("View All Details");
		}
	});
	// Have side block area follow scrolling
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
			}, 600, 'easeInOutExpo');
		} else {
			el.stop(true).animate({
				'top' : windowpos-100
			}, 600, 'easeInOutExpo');
		}
	});
	// Filtering block is an accordion
	$("#filtering_accordion").accordion({
		autoHeight: false
	});

	// Make the first ajax call for results automatically
	initiate_ajax_call();
});