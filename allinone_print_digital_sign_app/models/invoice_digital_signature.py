# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	is_sign_invoice = fields.Boolean(String="Allow Digital Signature for Customer Invoice")
	is_sign_bill = fields.Boolean(String="Allow Digital Signature for Vendor Bill")
	is_confirm_sign_invoice = fields.Boolean(string="Required Signature on Validate Customer Invoice",default=False)
	is_confirm_sign_bill = fields.Boolean(string="Required Signature on Validate Vendor Bill",default=False)

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(
			is_sign_invoice=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_invoice')),
			is_sign_bill=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_bill')),
			is_confirm_sign_invoice=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_invoice')),
			is_confirm_sign_bill=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_bill')),
		)
		return res

	@api.multi
	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_sign_invoice',self.is_sign_invoice),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_sign_bill',self.is_sign_bill),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_confirm_sign_invoice',self.is_confirm_sign_invoice),
		self.env['ir.config_parameter'].sudo().set_param('digital_signature.is_confirm_sign_bill',self.is_confirm_sign_bill),


class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	@api.model
	def _digital_sign_customer_invoice(self):
		is_sign_invoice=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_invoice'))
		return is_sign_invoice

	@api.model
	def _digital_sign_vendor_bill(self):
		is_sign_bill=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_sign_bill'))
		return is_sign_bill

	@api.model
	def _confirmation_digital_sign_customer_invoice(self):
		is_confirm_sign_invoice=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_invoice'))
		return is_confirm_sign_invoice

	@api.model
	def _confirmation_digital_sign_vendor_bill(self):
		is_confirm_sign_bill=(self.env['ir.config_parameter'].sudo().get_param('digital_signature.is_confirm_sign_bill'))
		return is_confirm_sign_bill

	@api.multi
	def action_invoice_open(self):
		res = super(AccountInvoice,self).action_invoice_open()
		if self.type == 'out_invoice':
			if self.confirm_sign_invoice_compute:
				if self.digital_signature is None:
					raise UserError(_('Please add Digital Signature for validate customer invoice...!'))
				else:
					return res
			else:
				return res
		elif self.type == 'in_invoice':
			if self.confirm_sign_bill_compute:
				if self.digital_signature is None:
					raise UserError(_('Please add Digital Signature for validate vendor bill...!'))
				else:
					return res
			else:
				return res
		else:
			return res

	digital_signature=fields.Binary(string="Digital Signature")
	sign_invoice_compute = fields.Text(default=_digital_sign_customer_invoice)
	digital_sign_vendor_bill_compute = fields.Text(default=_digital_sign_vendor_bill)
	confirm_sign_invoice_compute = fields.Text(default=_confirmation_digital_sign_customer_invoice)
	confirm_sign_bill_compute = fields.Text(default=_confirmation_digital_sign_vendor_bill)