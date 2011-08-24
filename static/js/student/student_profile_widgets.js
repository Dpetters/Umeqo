$(document).ready(function(){    
    $("#id_looking_for").multiselect({
        noneSelectedText: 'select job types',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        click: function(){
            $("#id_looking_for").trigger("change");
        },
        checkAll: function(){
            $("#id_looking_for").trigger("change");
        },
        uncheckAll: function(){
            $("#id_looking_for").trigger("change");
        }
    }).multiselectfilter();  
    
    $("#id_industries_of_interest").multiselect({
        noneSelectedText: 'select industries',
        classes: 'interested_in_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            $("#id_industries_of_interest").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > INDUSTRIES_OF_INTEREST_MAX ) {
                place_multiselect_warning_table($("#id_industries_of_interest"), MAX_INDUSTRIES_OF_INTEREST_EXCEEDED);
                return false;
            }
        },
        checkAll: function(){
            $("#id_industries_of_interest").trigger("change");
        },
        uncheckAll: function(){
            $("#id_industries_of_interest").trigger("change");
        }
    }).multiselectfilter();

    $("#id_previous_employers").multiselect({
        noneSelectedText: 'select employers',
        classes: 'previous_employers_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            $("#id_previous_employers").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > PREVIOUS_EMPLOYERS_MAX ) {
                place_multiselect_warning_table($("#id_previous_employers"), MAX_PREVIOUS_EMPLOYERS_EXCEEDED);
                return false;
            }
        },
        checkAll: function(){
            $("#id_previous_employers").trigger("change");
        },
        uncheckAll: function(){
            $("#id_previous_employers").trigger("change");
        }
    }).multiselectfilter();

    $("#id_campus_involvement").multiselect({
        noneSelectedText: 'select campus organizations',
        classes: 'campus_involvement_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        beforeoptgrouptoggle: function(e, ui){
            $(".warning").remove();
            if( ui.inputs.length - $(ui.inputs).filter(':checked').length + $(this).multiselect("widget").find("input:checked").length > CAMPUS_INVOLVEMENT_MAX ) {
                place_multiselect_warning_table($("#id_campus_involvement"), MAX_CAMPUS_INVOLVEMENT_EXCEEDED);
                return false;
            }
        },
        minWidth:multiselectMinWidth,
        height:146,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e, ui) {
            $(".warning").remove();
            $("#id_campus_involvement").trigger("change");
            if( ui.checked && $(this).multiselect("widget").find("input:checked").length > CAMPUS_INVOLVEMENT_MAX ) {
                place_multiselect_warning_table($("#id_campus_involvement"), MAX_CAMPUS_INVOLVEMENT_EXCEEDED);
                return false;
            }
        },
        checkAll: function(){
            $("#id_campus_involvement").trigger("change");
        },
        uncheckAll: function(){
            $("#id_campus_involvement").trigger("change");
        }
    }).multiselectfilter();
    
    $("#id_languages").multiselect({
        noneSelectedText: 'select languages',
        classes: 'languages_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:multiselectMinWidth,
        height:146,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(event, ui) {
            $(".warning").remove();
            $("#id_languages").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > LANGUAGES_MAX ) {
                place_multiselect_warning_table($("#id_languages"), MAX_LANGUAGES_EXCEEDED);
                return false;
            }
            var num = $(this).multiselect("widget").find("input:checked").filter(function(){
                 if(this.title.split(' (')[0] == ui.text.split(' (')[0])
                     return true;
               }).length;
               if (num > 1){
                   place_table_form_field_error($("<label class='warning' for'" + $("#id_languages").attr("id") + "'>" + ONE_LANGUAGE_DIFFICULTY + "</label>"), $("#id_languages"));
                   return false;
               }
        },
        checkAll: function(){
            $("#id_languages").trigger("change");
        },
        uncheckAll: function(){
            $("#id_languages").trigger("change");
        }
    }).multiselectfilter();

    $("#id_countries_of_citizenship").multiselect({
        noneSelectedText: "select countries",
        classes: 'countries_of_citizenship_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        height:146,
        minWidth:multiselectMinWidth,
        selectedList: 1,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            $("#id_countries_of_citizenship").trigger("change");
            if( $(this).multiselect("widget").find("input:checked").length > COUNTRIES_OF_CITIZENSHIP_MAX ) {
                place_multiselect_warning_table($("#id_countries_of_citizenship"), COUNTRIES_OF_CITIZENSHIP_MAX);
                return false;
            }
        },
        checkAll: function(){
            $("#id_countries_of_citizenship").trigger("change");
        },
        uncheckAll: function(){
            $("#id_countries_of_citizenship").trigger("change");
        }
    }).multiselectfilter(); 
});