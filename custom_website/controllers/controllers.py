# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute

_logger = logging.getLogger(__name__)

class CustomWebsiteSale(WebsiteSale):

    @http.route('/rop', type='http', auth="public", website=True, multilang=False, sitemap=False)
    def rop(self, **post):
        products = request.env['product.template'].search([('qty_available','<',5)])
        if products:
            values= {'products':products}

        return request.render("custom_website.rop_view", values)

    @http.route('/rop-real-time', type='http', auth="public", website=True, multilang=False, sitemap=False)
    def rop_real_time(self, **post):
        products = request.env['product.template'].search([('qty_available','>',5)])
        if products:
            values= {'products':products}

        return request.render("custom_website.real_time_view", values)


class RCCWebsiteController(http.Controller):

    @http.route(['/rop/update-qty'], type='json', auth="public", website=True)
    def demo_request(self, **post):
        result = {'status':False}
        """ Changes the Product Quantity by creating/editing corresponding quant.
        """
        warehouse = request.env['stock.warehouse'].search(
            [('company_id', '=', request.env.company.id)], limit=1
        )
        product = post.get('product')
        product_id = request.env['product.product'].search([('product_tmpl_id','=',product)])
        qty = post.get('qty')
        request.env['stock.quant'].with_context(inventory_mode=True).create({
            'product_id': product_id.id,
            'location_id': warehouse.lot_stock_id.id,
            'inventory_quantity': qty,
        })._apply_inventory()
        product_id = request.env['product.template'].search([('id','=',product)])
        #  check the qty updated and send the notification
        if product_id.qty_available == qty:
            result['status'] = True
            group_id = request.env.ref('stock.group_stock_manager').users
            partners_ids = group_id.mapped('partner_id').ids
            
            masaage = format(product_id.name) + ' his quantity updated successfully' 
            for partenr in partners_ids:
                if partner != request.env.user.partner_id:
                    messae_id = request.env['mail.message'].sudo().create({
                        'message_type': 'notification',
                        'body':masaage,
                        'subject':'Update Qty',
                        'partner_ids':partenr.id,
                       

                        })
                    request.env['mail.notification'].sudo().create({
                        'mail_message_id':messae_id.id,
                        'notification_type':'inbox',
                        'res_partner_id':partenr.id,
                        })
        return result

    