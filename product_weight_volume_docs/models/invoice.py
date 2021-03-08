# -*- coding: utf-8 -*-
# @author Carlos A. Garcia

from odoo import api, fields, models
from datetime import datetime, date

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    weight = fields.Float(compute='_compute_weight', string='Peso', readonly=True, help='El peso del producto sin incluir empaquetado.', default=0, store=False)
    volume = fields.Float(compute='_compute_volume', string='Volumen', readonly=True, help='El volumen del producto sin incluir empaquetado.', default=0, store=False)

    @api.depends('quantity')
    def _compute_weight(self):
        for line in self:
            weight = line.product_id.weight * line.quantity
            line.update({
                'weight': weight,
            })

    @api.depends('quantity')
    def _compute_volume(self):
        for line in self:
            vol = line.product_id.volume * line.quantity
            line.update({
                'volume': vol,
            })


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    total_weight = fields.Float(compute='_compute_total_weight', string='Peso Total', readonly=True, help='Peso total de la orden sin incluir empaquetado.', default=0, store=False)
    total_volume = fields.Float(compute='_compute_total_volume', string='Volumen Total', readonly=True, help='Volumen total de la orden sin incluir empaquetado.', default=0, store=False)
    commitment_date = fields.Char(compute='_compute_commitment_date', string='Fecha de compromiso', readonly=True, store=False)

    @api.depends('invoice_line_ids.weight')
    def _compute_total_weight(self):
        for invoice in self:
            weight = 0.0
            for line in invoice.invoice_line_ids:
                weight += line.weight
            invoice.update({
                'total_weight': weight,
            })

    @api.depends('invoice_line_ids.volume')
    def _compute_total_volume(self):
        for invoice in self:
            vol = 0.0
            for line in invoice.invoice_line_ids:
                vol += line.volume
            invoice.update({
                'total_volume': vol,
            })

    @api.depends('origin')
    def _compute_commitment_date(self):
        for invoice in self:
            if invoice.origin:
                sale_obj = self.env['sale.order'].search([('name','=',invoice.origin)])
                date = sale_obj.commitment_date if sale_obj else False
                if date:
                    invoice.commitment_date = date.strftime("%d/%m/%Y")
