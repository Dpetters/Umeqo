$(document).ready(function(){
    $(".resume_book_capacity_reached, .resume_book_capacity_reached_menu_button").tipsy({'gravity':'w', opacity: 0.9, live:true, fallback:RESUME_BOOK_CAPACITY_REACHED, html:true});
    $(".student_list_multiselect .ui-multiselect-disabled").tipsy({'gravity':'w', opacity: 0.9, live:true, fallback:STUDENT_LIST_REQUIRES_SUBSCRIPTION, html:true});
    
    $("#id_majors").multiselect({
        noneSelectedText: 'Filter By Major',
        selectedText: 'Filtering by # Majors',  
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        height: 192,
        checkAll: function() {
            page = 1;
            courses = $("#id_majors").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            courses = $("#id_majors").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 145,
        checkAll: function() {
            page = 1;
            school_years = $("#id_school_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            school_years = $("#id_school_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 145,
        checkAll: function() {
            page = 1;
            graduation_years = $("#id_graduation_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            graduation_years = $("#id_graduation_years").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 97,
        checkAll: function() {
            page = 1;
            employment_types = $("#id_employment_types").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            employment_types = $("#id_employment_types").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 174,
        checkAll: function() {
            page = 1;
            previous_employers = $("#id_previous_employers").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            previous_employers = $("#id_previous_employers").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 144,
        checkAll: function() {
            page = 1;
            industries_of_interest = $("#id_industries_of_interest").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            industries_of_interest = $("#id_industries_of_interest").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 196,
        checkAll: function() {
            page = 1;
            campus_orgs = $("#id_campus_involvement").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            campus_orgs = $("#id_campus_involvement").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
            campus_orgs = $("#id_campus_involvement").multiselect("getChecked").map( function() {
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
        minWidth:multiselectMinWidth,
        height: 168,
        checkAll: function() {
            page = 1;
            languages = $("#id_languages").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            languages = $("#id_languages").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
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
        minWidth:multiselectMinWidth,
        height: 142,
        checkAll: function() {
            page = 1;
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        uncheckAll: function() {
            page = 1;
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        },
        click: function(event, ui) {
            page = 1;
            countries_of_citizenship = $("#id_countries_of_citizenship").multiselect("getChecked").map( function() {
                return this.value;
            }).get();
            initiate_ajax_call();
        }
    }).multiselectfilter();
    
    $("#id_older_than_21").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        height: 53,
        minWidth:multiselectYesNoSingleSelectWidth,
        click: function(event, ui) {
            if (older_than_21 != ui.value){
                page = 1;
                older_than_21 = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#id_ordering").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        height: 82,
        minWidth:multiselectSingleSelectWidth,
        click: function(event, ui) {
            if (ordering != ui.value){
                page = 1;
                ordering = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#id_results_per_page").multiselect({
        header:false,
        selectedList: 1,
        multiple: false,
        height: 106,
        minWidth:multiselectSingleSelectWidth,
        click: function(event, ui) {
            if(results_per_page != ui.value){
                page = 1;
                results_per_page = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#gpa_filter_section div").slider({
        min: 0,
        max: 5.0,
        step: .1,
        value: 0.0,
        slide: function(event, ui) { $("#id_gpa").val(formatNumber(ui.value, 1,' ','.','','','-','').toString()); },
        change: function(event, ui) {
            if (min_gpa != ui.value) {
                page = 1;
                min_gpa = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#sat_t_filter_section div").slider({
        min: 600,
        max: 2400,
        step: 10,
        value: 600,
        slide: function(event, ui) { $("#id_sat_t").val(ui.value); },
        change: function(event, ui) {
            if (min_sat_t != ui.value) {
                page = 1;
                min_sat_t = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#sat_m_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) { $("#id_sat_m").val(ui.value); },
        change: function(event, ui) {
            if (min_sat_m != ui.value) {
                page = 1;
                min_sat_m = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#sat_v_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) { $("#id_sat_v").val(ui.value); },
        change: function(event, ui) {
            if (min_sat_v != ui.value) {
                page = 1;
                min_sat_v = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#sat_w_filter_section div").slider({
        min: 200,
        max: 800,
        step: 10,
        value: 200,
        slide: function(event, ui) { $("#id_sat_w").val(ui.value); },
        change: function(event, ui) {
            if (min_sat_w != ui.value) {
                page = 1;
                min_sat_w = ui.value;
                initiate_ajax_call();
            }
        }
    });
    $("#act_filter_section div").slider({
        min: 0,
        max: 36,
        step: 1,
        value: 0,
        slide: function(event, ui) { $("#id_act").val(ui.value); },
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
});