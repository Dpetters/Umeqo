$(document).ready(function(){
    $("#id_offered_job_types").multiselect({
        noneSelectedText: 'select job types',
        checkAllText: multiselectCheckAllText,
        uncheckAllText: multiselectUncheckAllText,
        minWidth:250,
        height:100
    });
    $("#id_industries").multiselect({
        noneSelectedText: 'select industries',
        classes: 'industries_multiselect',
        uncheckAllText: multiselectUncheckAllText,
        minWidth:250,
        beforeclose: function() {
            $(".warning").remove();
        },
        click: function(e) {
            $(".warning").remove();
            if( $(this).multiselect("widget").find("input:checked").length > MAX_INDUSTRIES ) {
                place_multiselect_warning_table($("#id_industries"), MAX_INDUSTRIES_EXCEEDED);
                return false;
            }
        }
    }).multiselectfilter();
});