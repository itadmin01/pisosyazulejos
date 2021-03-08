# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	is_sign_sale = fields.Boolean(String="Show Digital Signature in Sale Order?")
	is_confirm_sign_sale = fields.Boolean("Required Signature on Confirm Sale Order")

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(
			is_sign_sale=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_sale')),
			is_confirm_sign_sale=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_sale'))
		)
		return res

	@api.multi
	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_sign_sale',self.is_sign_sale),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_confirm_sign_sale',self.is_confirm_sign_sale),


class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.model
	def _sign_sale_order(self):
		is_sign_sale=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_sale'))
		return is_sign_sale

	@api.model
	def _confirmation_digital_sign_sale_order(self):
		is_confirm_sign_sale=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_sale'))
		return is_confirm_sign_sale

	@api.multi
	def action_confirm(self):
		res = super(SaleOrder,self).action_confirm()
		if self.confirm_sign_compute:
			if self.digital_signature:
				return res
			else:
				raise UserError(_("Please add Digital Signature for confirm sale order...!"))
		else:
			return res
		return res

	digital_signature=fields.Binary(string="Digital Signature")
	sign_sale_compute = fields.Text(default=_sign_sale_order)
	confirm_sign_compute = fields.Text(default=_confirmation_digital_sign_sale_order)
