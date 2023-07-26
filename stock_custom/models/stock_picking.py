# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
	_inherit = 'stock.picking'

	@api.constrains('scheduled_date','picking_type_id')
	def picking_validation(self):
		if self.picking_type_id.code == 'outgoing' and \
			self.scheduled_date.date() < fields.Date.today():
			raise ValidationError(_("The delivery order can't be outdated.. "))

	