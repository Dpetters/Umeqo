$(document).ready(function() {
    for (var i=0; i<employer_ids.length; i++) {
        $('.employers_listing').eq(i).bind('click', {id: employer_ids[i], num: i}, loadEmployer)
    }
});

function loadEmployer(e) {
    var employer_id = e.data.id;
    $.get(EMPLOYERS_LIST_EL_URL, {id: employer_id}, function(data) {
        $('#employers_detail').html(data);
        var stateObj = {id: employer_id};
        history.pushState(stateObj, "employer "+employer_id, EMPLOYERS_LIST_URL+"?id="+employer_id);
        $('.selected').removeClass('selected');
        $('.employers_listing').eq(e.data.num).addClass('selected');
    });
}