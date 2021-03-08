# -*- coding: utf-8 -*-#
from odoo import fields,api,models

class TransporteCompras(models.Model):
    _name = "transport.ceompras"
    
    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id
    
    peso = fields.Float(string="Peso")
    folio = fields.Many2one("purchase.order", string="Folio")
    currency_id = fields.Many2one("res.currency",string="Currency",default=_default_currency)
    saldo_a_cobrar = fields.Monetary(string="Saldo a cobrar", currency_field='currency_id',store=True,)
    transporte_id = fields.Many2one("transporte", string="transport")
    saldo_cobrado = fields.Float(string="Saldo cobrado")
    regreso = fields.Selection([('entregado', 'Entregado'),
                                ('devuelto', 'Devuelto'),
                                ('entrega_parcial', 'Entrega Parcial'),
                                ],string="Regreso")
    observaciones = fields.Text(string="Observaciones")
    volumen = fields.Float(string="Volumen")
    flete = fields.Float(string="Flete", compute='_get_flete')
    precio = fields.Float(string="Precio")

    @api.onchange("folio")
    def total_amount(self):
     #   if self.folio.amount_total:
     #       self.saldo_a_cobrar = self.folio.amount_total
        if self.folio.total_weight:
            self.peso = self.folio.total_weight
        if self.folio.total_volume:
            self.volumen = self.folio.total_volume

    @api.depends('precio','volumen')
    @api.one
    def _get_flete(self):
        if self.precio:
            self.flete = self.precio * self.volumen

    @api.onchange("regreso")
    def _change_regreso(self):
        if self.regreso == 'devuelto':
            self.precio = 0