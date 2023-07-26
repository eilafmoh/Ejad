odoo.define("custom_website.popup", function (require) {
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;
    function custom_popover(event, element_id, status, message) {

        element_id.popover({
            trigger: 'manual',
            container: 'body',
            template: '<div class="popover guest-checkout-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
            placement: 'bottom',
            animation: true,
            html: true,
            sanitize: false,
            content: `<p>` + message + `</p>`,

        });
        element_id.popover('show');
        setTimeout(function () { element_id.popover('dispose') }, 3000);
        
    }
    publicWidget.registry.rccContact = publicWidget.Widget.extend({
        selector: '.wrapper-section-demo',
        events: {

            'click #update-qty': '_onClick',
        },

        _onClick: function (ev) {
            var product = $(this.$target).find('input[name="product"]')

            $(ev.currentTarget).prop('disabled', true);
            var qty = $(this.$target).find('input[name="qty"]')
            console.log('ssssssssssss',product)
            
            if (!qty.val() ) {
                alert("Please Select add product qty");

            }
            
            else {
                var $self = $(this.$target)
                ajax.jsonRpc('/rop/update-qty', 'call', {
                    qty: qty.val(),
                    product:product.val(),
                    
                }).then(function (data) {
                    if (data.status == true) {
                        $self.find('#update-qty-form').remove();
                        $self.find('#rcc-wrapper-thanks-container').css('display', 'block');
                    }
                })
            }
        }


    });

    
})
