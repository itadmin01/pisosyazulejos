# -*- coding: utf-8 -*- #

from odoo import models, _
from odoo.exceptions import UserError
   
class StockMove(models.Model):
    _inherit = "stock.move"
    
    def action_show_details(self):
        res = super(StockMove, self).action_show_details()
        if res.get('context'):
            res['context'].update({'is_done_qty_popup' : True})
        return res
        
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if self._context.get('is_done_qty_popup'):
            for move in self:
                if round(move.quantity_done,4) > round(move.product_uom_qty,4):
                    raise UserError(_('No se puede tener una cantidad mayor que la demanda inicial'))
        return res
