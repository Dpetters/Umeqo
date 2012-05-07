var open_agree_to_terms_dialog = function () {
    var agree_to_terms_dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title: "Umeqo Terms Update",
        dialogClass: "agree_to_terms_dialog",
        resizable: false,
        modal: true,
        width: 400,
        closeOnEscape:false,
        close: function() {
            agree_to_terms_dialog.remove();
        }
    });
    agree_to_terms_dialog.dialog('open');
    $(".agree_to_terms_dialog .ui-dialog-titlebar-close").remove();
    
    agree_to_terms_dialog.html(DIALOG_AJAX_LOADER);

    var agree_to_terms_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
    $.ajax({
        dataType: "html",
        url: TERMS_AGREE_URL,
        complete : function(jqXHR, textStatus) {
            clearTimeout(agree_to_terms_dialog_timeout);
            agree_to_terms_dialog.dialog('option', 'position', 'center');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status==0){
                agree_to_terms_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
            }else{
                agree_to_terms_dialog.html(ERROR_MESSAGE_DIALOG);
            }
        },
        success: function (data) {
            agree_to_terms_dialog.html(data);
            $("#accept_terms").click(function(e){
                show_form_submit_loader(".agree_to_terms_dialog");
                $.ajax({
                    url: TERMS_AGREE_URL,
                    type:"POST",
                    complete:function(jqXHR, textStatus){
                       agree_to_terms_dialog.remove();
                    }
                });
                e.preventDefault();
                
            })
        }
    });
}

$(document).ready( function() {
    
    $(".needs_at_least_premium").tipsy({'gravity':'w', opacity: 0.9, live:true, fallback:NEEDS_AT_LEAST_PREMIUM, html:true}); 
    $(".needs_at_least_premium").tipsy({'gravity':'e', opacity: 0.9, live:true, fallback:NEEDS_AT_LEAST_PREMIUM, html:true}); 
    $(".needs_at_least_premium").tipsy({'gravity':'n', opacity: 0.9, live:true, fallback:NEEDS_AT_LEAST_PREMIUM, html:true}); 
    $(".needs_at_least_premium").tipsy({'gravity':'s', opacity: 0.9, live:true, fallback:NEEDS_AT_LEAST_PREMIUM, html:true}); 

    $('#account').click(function() {
       // We subtract two for the border
       $('#account_dropdown').width(document.getElementById("account").offsetWidth-2).toggle(); 
       if ($(this).hasClass('pressed')) $(this).removeClass('pressed');
       else $(this).addClass('pressed');
    });
    $('body').click(function(event) {
        if (!$(event.target).closest('#account').length && !$(event.target).closest('#account_dropdown').length) {
            $('#account_dropdown').hide();
            $('#account').removeClass('pressed');
        };
    }); 

    // NOTIFICATIONS.
    $('#notifications_count').click(function() {
        if (!$('#notifications_pane').is(':visible')) {
            $.get(NOTIFICATIONS_URL, function(data) {
                $('#notifications_pane').html(data);
            });
            $('#notifications_number').addClass('invisible');
            $('#notifications_count').addClass('pressed');
        } else {
            $('#notifications_count').removeClass('pressed');
        }
        $('#notifications_pane').toggle();
    });
    $(document).keydown(function(e) {
        if (e.which == 27) {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('pressed');
        }
    });
    $(document).click(function(e) {
        if ($(e.target).parents('#notifications_pane').length == 0 &&
            e.target.id != 'notifications_count') {
            $('#notifications_pane').hide();
            $('#notifications_count').removeClass('pressed');
        }
    });

    if (!AGREED_TO_TERMS && window.location.pathname != TERMS_URL){
        open_agree_to_terms_dialog();
    }
});