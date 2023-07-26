odoo.define('custom_pos.CashnowButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    var ajax = require('web.ajax');

    class CashnowButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            // to make instance payment with cash method
        }
    }
    CashnowButton.template = 'CashnowButton';

    ProductScreen.addControlButton({
        component: CashnowButton,
        condition: () => true,
    });

    Registries.Component.add(CashnowButton);

    return CashnowButton;
});
