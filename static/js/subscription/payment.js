$(document).ready(function() {
    
    Stripe.setPublishableKey('pk_HLhAnc2IezyC7awtBdNVhQvt2fE7B');
  
    $("#card_form").submit(function(event) {
        // disable the submit button to prevent repeated clicks
        $("#card_form input[type=submit]").attr("disabled", "disabled");
    
        Stripe.createToken({
            number: $('.card-number').val(),
            cvc: $('.card-cvc').val(),
            exp_month: $('.card-expiry-month').val(),
            exp_year: $('.card-expiry-year').val()
        }, stripeResponseHandler);
    
        // prevent the form from submitting with the default action
        return false;
    });
  
    function stripeResponseHandler(status, response) {
        if (response.error) {
            $("#card_form .error_section").text(response.error.message);
        } else {
            var form$ = $("#payment-form");
            // token contains id, last4, and card type
            var token = response['id'];
            // insert the token into the form so it gets submitted to the server
            form$.append("<input type='hidden' name='stripeToken' value='" + token + "'/>");
            // and submit
            form$.get(0).submit();
        }
    }
});