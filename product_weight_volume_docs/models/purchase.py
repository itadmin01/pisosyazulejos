# -*- coding: utf-8 -*-
# @author Carlos A. Garcia

from odoo import api, fields, models

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    weight = fields.Float(compute='_compute_weight', string='Peso', readonly=True, help='El peso del producto sin incluir empaquetado.', default=0, store=False)
    volume = fields.Float(compute='_compute_volume', string='Volumen', readonly=True, help='El volumen del producto sin incluir empaquetado.', default=0, store=False)

    @api.depends('product_uom_qty')
    def _compute_weight(self):
        for line in self:
            weight = line.product_id.weight * line.product_uom_qty
            line.update({
                'weight': weight,
            })

    @api.depends('product_uom_qty')
    def _compute_volume(self):
        for line in self:
            vol = line.product_id.volume * line.product_uom_qty
            line.update({
                'volume': vol,
            })

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    total_weight = fields.Float(compute='_compute_total_weight', string='Peso Total', readonly=True, help='Peso total de la orden sin incluir empaquetado.', default=0, store=False)
    total_volume = fields.Float(compute='_compute_total_volume', string='Volumen Total', readonly=True, help='Volumen total de la orden sin incluir empaquetado.', default=0, store=False)

    @api.depends('order_line.weight')
    def _compute_total_weight(self):
        for order in self:
            weight = 0.0
            for line in order.order_line:
                weight += line.weight
            order.update({
                'total_weight': weight,
            })

    @api.depends('order_line.volume')
    def _compute_total_volume(self):
        for order in self:
            vol = 0.0
            for line in order.order_line:
                vol += line.volume
            order.update({
                'total_volume': vol,
            })
