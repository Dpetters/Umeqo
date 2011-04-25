/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	/* Multiselect Widget Properties */
	var checkAllText = "All";
	var uncheckAllText = "None";
	var showAnimation = "";
	var hideAnimation = "";
	var minWidth = 318;
	var smallSingleSelectWidth = 182;
	var middleSingleSelectWidth = 202;
	var mediumHeight = 97;
	var largeHeight = 146;
	var twoOptionHeight = 47;
	
	/* Filtering Variables */
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


	function handle_multiselect_open_in_accordion(event, ui) {
		var parent = $(event.target).parents(".ui-accordion-content");
		var multiselect = $(event.target).multiselect('widget');
		var new_height = multiselect.height() + parseInt(multiselect.css('top'), 10);
		$(parent).css('height', new_height);
		//$(parent).animate({'height':new_height}, 200);
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

	function initiate_ajax_call() {
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
			$(".view_student_detailed_info_link").text("Show Details");
			$(".student_detailed_info").show('slow');
			$("#results_menu_toggle_details span").text("Hide All Details");
		} else {
			$(".view_student_detailed_info_link").text("Hide Details");
			$(".student_detailed_info").hide('slow');
			$("#results_menu_toggle_details span").text("View All Details");
		}
	});
	
	
	$("#id_student_list").multiselect({
		header:false,
		multiple: false,
		selectedList: 1,
		height:largeHeight,
		minWidth:minWidth
	});
	
	$("#id_majors").multiselect({
		noneSelectedText: 'Filter By Major',
		selectedText: 'Filtering by # Majors',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: largeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_school_years").multiselect({
		noneSelectedText: 'Filter By School Year',
		selectedText: 'Filtering by # School Years',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: mediumHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_graduation_years").multiselect({
		noneSelectedText: 'Filter By Graduation Year',
		selectedText: 'Filtering by # Graduation Years',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: mediumHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_employment_types").multiselect({
		noneSelectedText: 'Filter By Employment Type',
		selectedText: 'Filtering by # Employment Types',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: twoOptionHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});
	
	$("#id_previous_employers").multiselect({
		noneSelectedText: 'Filter By Previous Employers',
		selectedText: 'Filtering by # Previous Employers',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: largeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_industries_of_interest").multiselect({
		noneSelectedText: 'Filter By Industries of Interest',
		selectedText: 'Filtering by # Industries of Interest',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: largeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_languages").multiselect({
		noneSelectedText: 'Filter By Languages',
		selectedText: 'Filtering by # Languages',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: largeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();


	$("#id_campus_orgs").multiselect({
		noneSelectedText: 'Filter By Campus Organizations',
		selectedText: 'Filtering by # Campus Organizations',
		checkAllText: checkAllText,
		uncheckAllText: uncheckAllText,
		show: showAnimation,
		hide: hideAnimation,
		minWidth:minWidth,
		height: largeHeight,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	}).multiselectfilter();

	$("#id_older_than_18").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: showAnimation,
		hide: hideAnimation,
		height:twoOptionHeight,
		minWidth:smallSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_citizen").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: showAnimation,
		hide: hideAnimation,
		height:twoOptionHeight,
		minWidth:smallSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});
	
	$("#id_ordering").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: showAnimation,
		hide: hideAnimation,
		height:twoOptionHeight,
		minWidth:middleSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
	});

	$("#id_results_per_page").multiselect({
		header:false,
		selectedList: 1,
		multiple: false,
		show: showAnimation,
		hide: hideAnimation,
		height:twoOptionHeight,
		minWidth:middleSingleSelectWidth,
		open: handle_multiselect_open_in_accordion,
		close: handle_multiselect_close_in_accordion
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
			}, 600, 'easeInOutExpo');
		} else {
			el.stop(true).animate({
				'top' : windowpos-100
			}, 600, 'easeInOutExpo');
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