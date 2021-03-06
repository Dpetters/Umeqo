var handle_window_scroll = null;

function set_up_side_block_scrolling(element_id, offset, length) {
    var el = $(element_id);
    var elpos_original = el.offset().top;
    var scroll_side_block = function ( ) {
        var elpos = el.offset().top;
        var windowpos = $(window).scrollTop();
        var finaldestination = windowpos;
        if (windowpos<elpos_original) {
            finaldestination = elpos_original;
            el.stop(true).animate({
                    'top' : 0
                        }, length, 'easeInOutExpo');
        } else {
            el.stop(true).animate({
                    'top' : windowpos-offset
                }, length, 'easeInOutExpo');
        }
    };

    var handle_window_scroll = function () {
        if (this.scrollTO) {
            clearTimeout(this.scrollTO);
        }
        this.scrollTO = setTimeout(function () {
                $(this).trigger('scrollEnd');
            }, 100);
    };

    $(window).bind('scroll', handle_window_scroll);
    $(window).bind('scrollEnd', scroll_side_block);
}