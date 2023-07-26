import json
# import base64
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from odoo import api , fields, models,_
from odoo.exceptions import UserError
from datetime import datetime

class Ejad(http.Controller):

	# Show all Orders within start / end date
	@http.route('/show_orders', type='http', auth='public', methods=['GET'], csrf=False)
	def show_orders(self, **post):
		headers={'content-type':'application/json'} 
		try:
			start_date = post.get('start_date')
			end_date = post.get('end_date')
			orders = request.env['pos.order']
			start = datetime.strptime(start_date, '%m/%d/%Y').date()
			end = datetime.strptime(end_date, '%m/%d/%Y').date()
			ids = orders.sudo().search([])

			order_ids = []
			for order in ids:
				if order.date_order.date() >= start and \
				order.date_order.date() <= end:
					order_ids.append(order)

			orders_data = self.get_orders_data(order_ids)
			if not orders_data:
				raise UserError("no orders in selected period !")
			values = {
				'data' :orders_data ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)
	

	# Show all products that have ROP Count
	@http.route('/show_products_rop', type='http', auth='public', methods=['GET'], csrf=False)
	def show_products_rop(self):
		headers={'content-type':'application/json'} 
		try:
			products = request.env['product.template']
			product_ids = products.sudo().search([
				('has_rop','=',True),('rop_count','>',0)])
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
				'has_rop':product_id.has_rop,
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


	# Add A ROP Count for specific Product
	@http.route('/add_rop_count', type='http', auth='public', methods=['POST'], csrf=False)
	def add_rop_count(self , **post):
		headers={'content-type':'application/json'} 
		body = {}
		try:
			product = post.get('product_id')
			rop_count = post.get('rop_count')
			product_id = request.env['product.template'].sudo().search([('id','=',int(product)),('has_rop','=',True)])
			
			if not product_id:
				raise UserError("product not found or has no ROP count!")
			product_id.write({
				'rop_count':rop_count
			})
			values = {
				'data':{'product id':product_id.id,'product Name':product_id.name,'ROP Count':rop_count},
				'status':True,
				'message':'Success',
				'error_code':200
			}
			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	# Get all Orders inside a POS Session
	@http.route('/show_session_orders', type='http', auth='public', methods=['GET'], csrf=False)
	def show_session_orders(self, **post):
		headers={'content-type':'application/json'} 
		try:
			orders = request.env['pos.order']
			session = post.get('pos_session')
			order_ids = orders.sudo().search([('session_id','=',int(session))])
			orders_data = self.get_orders_data(order_ids)

			if not orders_data:
				raise UserError("no orders in selected session !")
			values = {
				'data' :orders_data ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}
			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)
	

	def get_orders_data(self,order_ids):
		orders_data = []
		for order_id in order_ids:
			lines = [{'product':line.full_product_name,'qty':line.qty, \
			'price':line.price_unit} for line in order_id.lines]

			payments = [{'payment method':line.payment_method_id.name,'amount':line.amount} \
			for line in order_id.payment_ids]

			order = {
				'id':order_id.id,
				'name':order_id.name,
				'session_id':{'id':order_id.session_id.id,'Session Name':order_id.session_id.name} if order_id.company_id else '',
				'user_id':{'id':order_id.user_id.id,'Session Name':order_id.user_id.name} if order_id.user_id else '',
				'lines':lines,
				'payments':payments,
				'pos_reference':order_id.pos_reference,
				'company_id':{'id':order_id.company_id.id , 'name':order_id.company_id.name} if order_id.company_id else '',
				}
			orders_data.append(order)
		return orders_data