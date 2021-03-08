# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64

class AccountPayment(models.Model):
    _inherit = 'account.payment'
        
    attachment_id = fields.Many2one("ir.attachment", 'Attachment')

    
    
