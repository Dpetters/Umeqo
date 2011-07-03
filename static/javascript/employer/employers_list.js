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
        startLoading();
        $.get(SEARCH_URL, {
            'q': query,
            'i': industry,
            'h': has_events,
            's': in_subscriptions
        }, function(data) {
            $('#employers_listings').html(data);
            bindLoadEmployerHandlers();
            stopLoading();
        });
    }
});

$('#employer_subscribe').live('click', function(e) {
    var loaded_id = $('#loaded_employer_id').val();
    $(this).html('<img src="' + STATIC_URL + 'images/page_elements/loaders/small_ajax_loader.gif" />');
    $(this).addClass('disabled-button');
    var that = $(this);
    $.post(SUBSCRIBE_URL, {id: loaded_id, subscribe: 1}, function(data) {
        that.html('Unsubscribe');
        that.attr('id','employer_unsubscribe');
        that.removeClass('disabled-button');
        that.addClass('warning-button');
    });
    e.preventDefault();
});

$('#employer_unsubscribe').live('click', function(e) {
    var loaded_id = $('#loaded_employer_id').val();
    $(this).html('<img src="' + STATIC_URL + 'images/page_elements/loaders/small_ajax_loader.gif" />');
    $(this).removeClass('warning-button');
    $(this).addClass('disabled-button');
    var that = $(this);
    $.post(SUBSCRIBE_URL, {id: loaded_id, subscribe: 0}, function(data) {
        that.html('Subscribe');
        that.attr('id','employer_subscribe');
        that.removeClass('disabled-button');
    });
    e.preventDefault();
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
    $.get(EMPLOYERS_LIST_PANE_URL, {id: id}, function(data) {
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
