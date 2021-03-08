# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    @api.multi
    def action_iniciar_transporte(self):
        env = api.Environment(self._cr, SUPERUSER_ID, {})
        facturas = env['transport.facturas'].search([])
        for factura in facturas:
            if factura.regreso == 'entregado':
                invoice = self.env['account.invoice'].search([('id','=',factura.folio.id)],limit=1)
                invoice.write({'entregado': True})
    
        compras = env['transport.ceompras'].search([])
        for compra in compras:
            if compra.regreso == 'entregado':
                invoice = self.env['purchase.order'].search([('id','=',compra.folio.id)],limit=1)
                invoice.write({'entregado': True})
    
        salidas = env['transport.transferencias'].search([])
        for salida in salidas:
            if salida.regreso == 'entregado':
                invoice = self.env['stock.picking'].search([('id','=',salida.folio.id)],limit=1)
                invoice.write({'entregado': True})
