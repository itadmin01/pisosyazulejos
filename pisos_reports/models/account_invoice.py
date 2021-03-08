# -*- coding: utf-8 -*- #
from odoo import fields,models,_,api
from odoo.exceptions import UserError, ValidationError

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    entregado = fields.Boolean(String="Entregado", default = False)
    
class StockPiking(models.Model):
    _inherit = "stock.picking"
    entregado = fields.Boolean(String="Entregado", default = False)
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    entregado = fields.Boolean(String="Entregado", default = False)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def select_customer_first(self):
        if not self.order_id.partner_id:
            raise UserError(_('Debe seleccionar primero un transportista'))
    
class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def select_customer_first(self):
        if not self.invoice_id.partner_id:
            raise UserError(_('Debe seleccionar primero un transportista'))