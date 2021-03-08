# -*- coding: utf-8 -*- #
from odoo import fields,models,_,api

class HrExpenseExtends(models.Model):
    _inherit = 'hr.expense'
    
    sequence = fields.Char(string='Sequence', default='New')
    proveedor_id = fields.Many2one('res.partner', string='Proveedor')
    
    @api.model
    def create(self,vals):
        if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('expense') or _('New')         
        result=super(HrExpenseExtends,self).create(vals)
        return result