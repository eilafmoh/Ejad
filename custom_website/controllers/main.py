import json
# import base64
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from odoo import api , fields, models,_
from odoo.exceptions import UserError
from datetime import datetime

class Products(http.Controller):

	# end-point that return all the product < 5 quantity
	@http.route('/rop-product', type='http', auth='public', methods=['GET'], csrf=False)
	def rop_product(self):
		headers={'content-type':'application/json'} 
		try:
			products = request.env['product.template']
			product_ids = products.sudo().search([
				('qty_available','<',5)])
			product_data = self.get_products_data(product_ids)

			values = {
				'data' :product_data ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)
	
	def get_products_data(self,product_ids):
		product_data = []
		for product_id in product_ids:
			img_url = self.get_product_image(product_id.id)
			product = {
				'id':product_id.id,
				'name':product_id.name,
				'qty_available':product_id.qty_available,
				'detailed_type':product_id.detailed_type,
				'rop_count':product_id.rop_count,
				'list_price':product_id.list_price,
				'standard_price':product_id.standard_price,
				'default_code':product_id.default_code,
				'categ_id':{'id':product_id.categ_id.id , 'name':product_id.categ_id.name} if product_id.categ_id.name else '',
				'img_url':img_url,
				}
			product_data.append(product)
		return product_data

	def get_product_image(self,product_id):
		if product_id:
			request.env.cr.execute(
				"SELECT id FROM ir_attachment WHERE res_model='product.template' and res_id=%s",
				[product_id]
			)
			if request.env.cr.fetchone():
				img_url = 'http://'+request.httprequest.__dict__['environ']['HTTP_HOST']+'/web/product_image/%s/image_1920/product.template' % product_id,
				return img_url[0]
			else:
				return '/'
		else:
			return '/'