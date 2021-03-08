# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	is_sign_inventory = fields.Boolean(String="Allow Digital Signature in Inventory")
	is_confirm_sign = fields.Boolean(string="Required Signature on Validate Inventory")
	sign_applicable_inside = fields.Selection([
		('picking', 'Picking Operation'),
		('delivery', 'Delivery Slip'),
		('both', 'Both'),
		], string="Allow Signature for")

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(
			is_sign_inventory=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_inventory')),
			is_confirm_sign=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign')),
			sign_applicable_inside=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.sign_applicable_inside')),

		)
		return res

	@api.multi
	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_sign_inventory',self.is_sign_inventory),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_confirm_sign',self.is_confirm_sign),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.sign_applicable_inside',self.sign_applicable_inside),


class StockPicking(models.Model):
	_inherit = "stock.picking"

	@api.model
	def _digital_sign_inventory(self):
		is_sign_inventory = (self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_inventory'))
		return is_sign_inventory

	@api.model
	def _confirmation_digital_sign_inventory(self):
		is_confirm_sign = (self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign'))
		return is_confirm_sign

	@api.model
	def _digital_sign_applicable_inside(self):
		sign_applicable_inside = (self.env['ir.config_parameter'].sudo().get_param('digital_signature.sign_applicable_inside'))
		return sign_applicable_inside

	@api.multi
	def button_validate(self):
		if self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign'):
			if self.digital_signature:
				return super(StockPicking,self).button_validate()
			else:
				raise UserError(_('Please add Digital Signature for validate inventory...!'))
		else:
			return super(StockPicking,self).button_validate()
		return super(StockPicking,self).button_validate()

	digital_signature = fields.Binary(string="Digital Signature")
	digital_sign_inventory_compute = fields.Text(default=_digital_sign_inventory)
	confirm_sign_inventory_compute = fields.Text(default=_confirmation_digital_sign_inventory)
	sign_applicable_inside = fields.Text(default=_digital_sign_applicable_inside)