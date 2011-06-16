$(document).ready(function() {
    for (var i=0; i<employer_ids.length; i++) {
        $('.employers_listing').eq(i).bind('click', {id: employer_ids[i], i: i}, loadEmployer)
    }
});

function loadEmployer(e, noPush) {
    var disablePush = noPush || false;
    var id = e.data.id;
    var i = e.data.i;
    $.get(EMPLOYERS_LIST_EL_URL, {id: id}, function(data) {
        $('#employers_detail').html(data);
        if (!disablePush) {
            var stateObj = {id: id, i: i};
            history.pushState(stateObj, "employer "+id, EMPLOYERS_LIST_URL+"?id="+id);
        }
        $('.selected').removeClass('selected');
        $('.employers_listing').eq(i).addClass('selected');
    });
}

window.onpopstate = function(event) {
    if (event.state != null) {
        var stateObj = {id: event.state.id, i: event.state.i};
        loadEmployer({data: stateObj}, true)
    } else if ($('#isnotajax').val()=='false') {
        var stateObj = {id: FIRST_EMPLOYER_ID, i: 0};
        loadEmployer({data: stateObj}, true);
    }
}