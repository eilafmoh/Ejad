odoo.define('custom_website.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosMercuryPaymentLines = (PaymentScreen) =>
        class extends PaymentScreen {
            /**
             * @override
             */
            selectedLineClass(line) {
                return Object.assign({}, super.selectedLineClass(line), {
                    o_pos_mercury_swipe_pending: line.mercury_swipe_pending,
                });
            }
            /**
             * @override
             */
            unselectedLineClass(line) {
                return Object.assign({}, super.unselectedLineClass(line), {
                    o_pos_mercury_swipe_pending: line.mercury_swipe_pending,
                });
            }
        };

    Registries.Component.extend(PaymentScreen, PosMercuryPaymentLines);

    return PaymentScreen;
});
