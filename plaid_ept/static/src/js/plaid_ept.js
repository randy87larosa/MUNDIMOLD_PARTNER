odoo.define('plaid_ept.plaid_ept', function (require) {
"use strict";

$(document).ready(function() {

    // var handler = Plaid.create({
    //     apiVersion: 'v2',
    //     clientName: 'Plaid Walkthrough Demo',
    //     env: 'sandbox',
    //     product: ['transactions'],
    //     key: 'f8cc0b5128dbb50679b613f41810c6',
    //     onSuccess: function(public_token) {
    //         $.post('/get_access_token', {public_token: public_token}, function() {
    //             $('#container').fadeOut('fast', function() {
    //                 $('#intro').hide();
    //                 $('#app, #steps').fadeIn('slow');
    //             });
    //         });
    //     },
    // });

    $('.o_form_view #plaid_ept').on('click', function(e) {
            alert("in");
            // handler.open();
    });

});

});
