// static/js/stripe.js

document.addEventListener('DOMContentLoaded', function () {
    var stripe = Stripe('pk_test_51PNepWP6s4WCFp1nJbw5BAQHML9ZnM7MbH7h2OXsjMp2GPCV1Ac6jfsvfQjIopK812M55B7bjTUjW5OhRFhJ5R1S00cLtrHrHw');
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');

    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        stripe.createToken(card).then(function (result) {
            if (result.error) {
                // Display error.message in your UI.
            } else {
                // Send the token to your server.
                stripeTokenHandler(result.token);
            }
        });
    });

    function stripeTokenHandler(token) {
        var form = document.getElementById('payment-form');
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        form.appendChild(hiddenInput);

        form.submit();
    }
});
