$(document).ready(function() {

    bindLoadEmployerHandlers();

    $('#employers_filter_name').keydown(function() {
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(filterEmployers,200);
    });

    $('#employers_filter_industry, #employers_filter_has_events').change(function() {
        filterEmployers();
    });

    function filterEmployers() {
        var query = $('#employers_filter_name').val();
        var industry = $('#employers_filter_industry').val();
        var has_events = $('#employers_filter_has_events').attr('checked');
        startLoading();
        $.get(SEARCH_URL,{
                'q': query,
                'i': industry,
                'h': has_events
            }, function(data) {
            $('#employers_listings').html(data);
            bindLoadEmployerHandlers();
            stopLoading();
        });
    }
});

function startLoading() {
    $('#employers_list_form').append('<div id="loading_div"></div>');
}

function stopLoading() {
    $('#loading_div').remove();
}


function bindLoadEmployerHandlers() {
    $('.employers_listing').each(function() {
        $(this).click(function() {
            var id = $(this).children('.employer_id').eq(0).val();
            loadEmployer(this, getID(this));
        });
    });
}

function getID(el) {
    return $(el).children('.employer_id').eq(0).val();
}

function loadEmployer(target, id, noPush) {
    var disablePush = noPush || false;
    var listing;
    if (!target) {
        $('.employers_listing').each(function() {
            if (getID(this) == id) {
                listing = this;
            }
        })
    } else {
        listing = target;
    }
    startLoading();
    $.get(EMPLOYERS_LIST_EL_URL, {id: id}, function(data) {
        $('#employers_detail').html(data);
        if (!disablePush) {
            var stateObj = {id: id};
            history.pushState(stateObj, "employer "+id, EMPLOYERS_LIST_URL+"?id="+id);
        }
        $('.selected').removeClass('selected');
        $(listing).addClass('selected');
        stopLoading();
    });
}

window.onpopstate = function(event) {
    if (event.state != null) {
        loadEmployer(null, event.state.id, true);
    } else if ($('#isnotajax').val()=='false') {
        var stateObj = {id: FIRST_EMPLOYER_ID, i: 0};
        loadEmployer(null, FIRST_EMPLOYER_ID, true);
    }
}
