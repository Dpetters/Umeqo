$(document).ready(function() {
    var last_four_digits = null;
    
    Stripe.setPublishableKey('pk_HLhAnc2IezyC7awtBdNVhQvt2fE7B');
  
    $("#card_form").submit(function(event) {
        // disable the submit button to prevent repeated clicks
        $("#card_form input[type=submit]").attr("disabled", "disabled");
        $("#card_form .error_section").text("");
        last_four_digits = $('#id_card_number').val() % 10000;
        Stripe.createToken({
            number: $('#id_card_number').val(),
            cvc: $('#id_card_cvc').val(),
            exp_month: $('#id_card_expiry_month').val(),
            exp_year: $('#id_card_expiry_year').val()
        }, stripeResponseHandler);
    
        // prevent the form from submitting with the default action
        return false;
    });
  
    function stripeResponseHandler(status, response) {
            $("#card_form input[type=submit]").removeAttr("disabled");
        if (response.error) {
            $("#card_form .error_section").text(response.error.message);
        } else {
            var form$ = $("#card_form");
            // token contains id, last4, and card type
            var token = response['id'];
            // insert the token into the form so it gets submitted to the server
            form$.append("<input type='hidden' name='stripe_token' value='" + token + "'/>");
            // insert the last 4 digits of the credit card number
            form$.append("<input type='hidden' name='last_4_digits' value='" + last_four_digits + "'/>");
            // and submit
            form$.get(0).submit();
        }
    }
    
    $("#change_payment a").live("click", function(){
        $(this).hide();
        $("#existing_card").hide();
        $("#card_form").removeClass("hid");
    });
});