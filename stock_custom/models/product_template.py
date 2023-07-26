# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	has_rop = fields.Boolean('Has ROP',default=False)
	rop_count = fields.Integer('ROP Count')
	count = fields.Integer(compute='get_count')

	@api.depends('has_rop')
	def get_count(self):
		self.count = self.search_count([('has_rop','=',True),
									('id','!=',self._origin.id)])


