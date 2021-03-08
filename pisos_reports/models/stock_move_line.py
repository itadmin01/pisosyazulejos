# -*- coding: utf-8 -*- #
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    
#     @api.onchange('qty_done')
#     def _onchange_qty_done(self):
#         res = super(StockMoveLine, self)._onchange_qty_done()
#         if self.qty_done > self.product_uom_qty:
#             raise UserError(_('Please do not enter Done quantity is higher than Reserved quantity'))
#         return res
