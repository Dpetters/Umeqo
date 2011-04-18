/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

    /* FILTERING VARIABLES */
    var gpa = 0;
    var act = 0;
    var sat_t = 600;
    var sat_m = 200;
    var sat_v = 200;
    var sat_w = 200;
    var page = 1;
    var ordering = $("#id_ordering option:selected").val();
    var results_per_page = $("#id_results_per_page option:selected").val();
    var courses = new Array();

    var prev_multiselect_height = 0;

    $("#id_campus_orgs").multiselect({
        noneSelectedText: 'Filter By Campus Organizations',
        selectedText: 'Filtering by # Campus Organizations',
        checkAllText: "All",
        minWidth:305,
        height: 125,
        open: function(event, ui) {
            var parent = $("#id_campus_orgs").parents(".ui-accordion-content");
            $(parent).css('height', $("#id_campus_orgs").nextAll(".ui-multiselect-menu").height()+85);
        },
        uncheckAllText: "None",
        close: function(e) {
            $("#id_campus_orgs").parents(".ui-accordion-content").css("height", "");
        },
    }).multiselectfilter();

    $("#id_school_years").multiselect({
        noneSelectedText: 'Filter By School Year',
        selectedText: 'Filtering by # School Years',
        checkAllText: "All",
        minWidth:305,
        height: 62,
        open: function(event, ui) {
            var parent = $("#id_school_years").parents(".ui-accordion-content");
            $(parent).css('height', $("#id_school_years").nextAll(".ui-multiselect-menu").height()+110);
        },
        uncheckAllText: "None",
        close: function(e) {
            $("#id_school_years").parents(".ui-accordion-content").css("height", "");
        },
    }).multiselectfilter();

    $("#id_languages").multiselect({
        noneSelectedText: 'Filter By Languages',
        selectedText: 'Filtering by # Languages',
        checkAllText: "All",
        minWidth:305,
        height: 120,
        uncheckAllText: "None",
    }).multiselectfilter();

    $("#id_previous_employers").multiselect({
        noneSelectedText: 'Filter By Previous Employers',
        selectedText: 'Filtering by # Previous Employers',
        checkAllText: "All",
        minWidth:305,
        height: 90,
        uncheckAllText: "None",
    }).multiselectfilter();

    $("#id_industries_of_interest").multiselect({
        noneSelectedText: 'Filter By Industries of Interest',
        selectedText: 'Filtering by # Industries of Interest',
        checkAllText: "All",
        minWidth:305,
        height: 70,
        uncheckAllText: "None",
    }).multiselectfilter();

    $("#id_grad_years").multiselect({
        noneSelectedText: 'Filter By Graduation Year',
        selectedText: 'Filtering by # Graduation Years',
        checkAllText: "All",
        minWidth:305,
        height: 62,
        open: function(event, ui) {
            var parent = $("#id_grad_years").parents(".ui-accordion-content");
            $(parent).css('height', $("#id_grad_years").nextAll(".ui-multiselect-menu").height()+135);
        },
        uncheckAllText: "None",
        close: function(e) {
            $("#id_grad_years").parents(".ui-accordion-content").css("height", "");
        },
    }).multiselectfilter();

    $("#id_majors").multiselect({
        noneSelectedText: 'Filter By Major',
        selectedText: 'Filtering by # Majors',
        checkAllText: "All",
        minWidth:305,
        height: 100,
        open: function(event, ui) {
            var parent = $("#id_majors").parents(".ui-accordion-content");
            $(parent).css('height', $("#id_majors").nextAll(".ui-multiselect-menu").height()+60);
        },
        uncheckAllText: "None",
        close: function(e) {
            $("#id_majors").parents(".ui-accordion-content").css("height", "");
        },
    }).multiselectfilter();

    $("#id_school_years").multiselect({
        noneSelectedText: 'Filter By School Year',
        selectedText: 'Filtering by # School Years',
        checkAllText: "All",
        minWidth:305,
        height: 62,
        open: function(event, ui) {
            var parent = $("#id_school_years").parents(".ui-accordion-content");
            $(parent).css('height', $("#id_school_years").nextAll(".ui-multiselect-menu").height()+110);
        },
        uncheckAllText: "None",
        close: function(e) {
            $("#id_school_years").parents(".ui-accordion-content").css("height", "");
        },
    }).multiselectfilter();
    
    $("#id_ordering").multiselect({
        height:47,
        header:false,
        minWidth:190,
        selectedList: 1,
        multiple: false
    });

    $("#id_results_per_page").multiselect({
        height:47,
        header:false,
        minWidth:187,
        selectedList: 1,
        multiple: false
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

    $("#search_form_submit_button").live('click', initiate_search);

    var el = $('#info_block');
    var elpos_original = el.offset().top;

    $(window).scroll( function() {
        var elpos = el.offset().top;
        var windowpos = $(window).scrollTop();
        var finaldestination = windowpos;
        if(windowpos<elpos_original) {
            finaldestination = elpos_original;
            el.stop(true).animate({'top' : 0}, 600, 'easeInOutExpo');
        } else {
            el.stop(true).animate({'top' : windowpos-100}, 600, 'easeInOutExpo');
        }
    });
    $("#filtering_accordion").accordion({ autoHeight: false });

    // Starts Search
    function initiate_search() {
        var search_query = $("#query_field").val();
        if(search_query != "Search by keywords, skills, etc" && search_query != "") {
            query = search_query.replace(/[^a-z\d ]+/ig,'');
        }
        initiate_ajax_call();
    };

    $(".campus_org_link").live('click', campus_org_click)
    function campus_org_click() {

    };

    $("#id_results_per_page").change( function() {
        results_per_page = $("#id_results_per_page option:selected").val();
        initiate_ajax_call();
    });
    $("#id_ordering").change( function() {
        ordering = $("#id_ordering option:selected").val();
        initiate_ajax_call();
    });
    // Opens Dialog
    function open_dialog() {
        var dialog = $('<div></div>')
        .html('<img class="spinner" title="Loading" src="/static/images/page_elements/loaders/loader.gif" alt="Loading...">')
        .dialog({
            autoOpen: false,
            title: this.id,
            resizable: false,
            width: 650,
            height: 300,
            maxWidth: 500
        });
        dialog.dialog('open');
        return dialog;
    };

    function course_click() {
        var dialog = open_dialog();
        $.get("/get_course_info/", {'course_name': this.id}, function(data) {
            var content = "<img align='left' class='image' src='/static/"+data['image'] + "' title=" + data['name'] + " alt=" + data['name'] + ">" +
            "<p class='content_info'><strong>Course Number: </strong>" + data['num'] + "</p>" +
            "<p class='content_info'><strong>Department Head: </strong>" + data['admin'] + "</p>" +
            "<p class='content_info'><strong>Contact Email: </strong>" + data['email'] + "</p>" +
            "<p class='content_info'><strong>Website: </strong>" + data['email'] + "</p>" +
            "<p class='content_info'><strong>Course Description: </strong>" + data['description'] + "</p>";
            dialog.html(content);
        }, "json");
        return false;
    };

    $(".course_link").live('click', course_click);

    $(".page_link").live('click', function() {
        page = $(this).attr("id").substring(5);
        initiate_ajax_call();
    });
    $("#gpa_filter div").slider({
        min: 0,
        max: 5.0,
        step: .1,
        value: 0,
        slide: function(event, ui) {
            $("#gpa_value").val(ui.value);
        },
        change: function(event, ui) {
            if (gpa != ui.value) {
                page = 1;
                gpa = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //SAT Total Slider
    $("#sat_t_filter div").slider({
        min: 600,
        max: 2400,
        step: 10,
        value: 600,
        slide: function(event, ui) {
            $("#sat_t_value").val(ui.value);
        },
        change: function(event, ui) {
            if (sat_t != ui.value) {
                page = 1;
                sat_t = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //SAT M Slider
    $("#sat_m_filter div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#sat_m_value").val(ui.value);
        },
        change: function(event, ui) {
            if (sat_m != ui.value) {
                page = 1;
                sat_m = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //SAT V Slider
    $("#sat_v_filter div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#sat_v_value").val(ui.value);
        },
        change: function(event, ui) {
            if (sat_v != ui.value) {
                page = 1;
                sat_v = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //SAT W Slider
    $("#sat_w_filter div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) {
            $("#sat_w_value").val(ui.value);
        },
        change: function(event, ui) {
            if (sat_w != ui.value) {
                page = 1;
                sat_w = ui.value;
                initiate_ajax_call();
            }
        }
    });

    //ACT Slider
    $("#act_filter div").slider({
        min: 0,
        max: 36,
        step: 1,
        value: 0,
        slide: function(event, ui) {
            $("#act_value").val(ui.value);
        },
        change: function(event, ui) {
            if (act != ui.value) {
                page = 1;
                act = ui.value;
                initiate_ajax_call();
            }
        }
    });

    // Set up filtering values
    $("#gpa_value").val($("#gpa_filter div").slider("value"));
    $("#act_value").val($("#act_filter div").slider("value"));
    $("#sat_t_value").val($("#sat_t_filter div").slider("value"));
    $("#sat_m_value").val($("#sat_m_filter div").slider("value"));
    $("#sat_w_value").val($("#sat_w_filter div").slider("value"));
    $("#sat_v_value").val($("#sat_v_filter div").slider("value"));

    $("#resume_book_block .side_block_content").droppable({
        activeClass: "add_to_resume_book_area_active",
        hoverClass: "add_to_resume_book_area_hover",
        drop: function(event, ui) {
            $.ajax({'url':'/employer/add-to-resume-book/' + $(ui.draggable).attr("id").substring(4) + "/",
                success: function(date) {
                }});
        }
    });

    var initiate_ajax_call = function() {
        $("#results_section").css('opacity', 0.5);
        $("#results_block_loader_section").css('display', 'block');
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
            },
            type: 'POST',
            url: '/employer/results/',
            data: {'results_per_page':1,
                'query': query,
                'gpa' : gpa,
                'act':act,
                'page':page,
                'sat_t' : sat_t,
                'sat_m': sat_m,
                'sat_v': sat_v,
                'sat_w': sat_w,
                'ordering': ordering,
                'results_per_page': results_per_page,
                'courses' : courses},
            dataType: "html",
            success: function (data) {
                $('#results_section').html(data);

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
                    }});
                $("#results_section").css('opacity', 1);
                $("#results_block_loader_section").css('display', 'none');
            }
        });
    };
    $("#results_menu_checkbox").live('click', function() {
        if($("#results_menu_checkbox").attr('checked')==false) {
            $(".student_checkbox:checked").each( function() {
                $(this).attr('checked', false);
            }
            );
        } else {
            $(".student_checkbox").not(':checked').each( function() {
                $(this).attr('checked', true);
            }
            );
        }
    });
    
    /* Results Menu Bar */
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
    initiate_ajax_call();
});