$(document).ready(function() {
    Stripe.setPublishableKey(STRIPE_PUBLISHABLE_KEY);

    function stripeResponseHandler(status, response) {
        if (response.error) {
            $("form input[type=submit]").removeAttr("disabled");
            $("form .error_section").text(response.error.message);
            hide_form_submit_loader("form");
        } else {
            var form$ = $("form");
            // token contains id, last4, and card type
            var token = response['id'];
            // insert the token into the form so it gets submitted to the server
            form$.append("<input type='hidden' name='stripe_token' value='" + token + "'/>");
            // and submit
            form$.get(0).submit();
        }
    }

    $("form").submit(function(event) {
        $("form input[type=submit]").attr("disabled", "disabled");
        show_form_submit_loader("form");
        $("form .error_section").text("");
        if(!$("#card_fields").hasClass("hid")){
            Stripe.createToken({
                number: $('#id_card_number').val(),
                cvc: $('#id_card_cvc').val(),
                exp_month: $('#id_card_expiry_month').val(),
                exp_year: $('#id_card_expiry_year').val()
            }, stripeResponseHandler);
            return false
        }
    });
});