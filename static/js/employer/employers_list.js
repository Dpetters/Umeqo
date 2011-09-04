$(document).ready(function() {

    bindLoadEmployerHandlers();

    $('#employers_filter_name').keydown(function() {
        if (typeof timeoutID!='undefined') window.clearTimeout(timeoutID);
        timeoutID = window.setTimeout(filterEmployers,200);
    });

    $('#employers_filter_industry, #employers_filter_has_events, #employers_filter_in_subscriptions').change(function() {
        filterEmployers();
    });

    function filterEmployers() {
        var query = $('#employers_filter_name').val();
        var industry = $('#employers_filter_industry').val();
        var has_events = $('#employers_filter_has_events').attr('checked');
        var in_subscriptions = $('#employers_filter_in_subscriptions').attr('checked');
        show_form_submit_loader("#employers_list_form");
        $.get(SEARCH_URL, {
            'q': query,
            'i': industry,
            'h': has_events,
            's': in_subscriptions
        }, function(data) {
            $('#employers_listings').html(data);
            bindLoadEmployerHandlers();
            hide_form_submit_loader("#employers_list_form");
        });
    }
});

$('#employer_subscribe').live('click', function(e) {
    var loaded_id = $('#loaded_employer_id').val();
    $(this).html('<img src="' + STATIC_URL + 'images/loaders/s_ajax_transparent.gif" />');
    $(this).attr('disabled', 'disabled');
    var that = $(this);
    $.post(SUBSCRIBE_URL, {id: loaded_id, subscribe: 1}, function(data) {
        that.html('Unsubscribe');
        that.attr('id','employer_unsubscribe');
        that.removeAttr('disabled');
        that.addClass('warning-button');
    });
    e.preventDefault();
});

$('#employer_unsubscribe').live('click', function(e) {
    var loaded_id = $('#loaded_employer_id').val();
    $(this).html('<img src="' + STATIC_URL + 'images/loaders/s_ajax_transparent.gif" />');
    $(this).removeClass('warning-button');
    $(this).attr('disabled', 'disabled');
    var that = $(this);
    $.post(SUBSCRIBE_URL, {id: loaded_id, subscribe: 0}, function(data) {
        that.html('Subscribe');
        that.attr('id','employer_subscribe');
        that.removeAttr('disabled')
    });
    e.preventDefault();
});
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
    show_form_submit_loader("#employers_list_form");
    $.get(EMPLOYERS_LIST_PANE_URL, {id: id}, function(data) {
        $('#employers_detail').html(data);
        if (!disablePush) {
            var stateObj = {id: id};
            history.pushState(stateObj, "employer "+id, EMPLOYERS_LIST_URL+"?id="+id);
        }
        $('.selected').removeClass('selected');
        $(listing).addClass('selected');
        hide_form_submit_loader("#employers_list_form");
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
