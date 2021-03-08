# -*- coding: utf-8 -*- #
from odoo import fields,models,api,_
from odoo.exceptions import UserError

class Transporte(models.Model):
    _name = "transporte"

    name = fields.Char(string="Draft Invoice" , default='New',readonly=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('valid', 'Validado'),
        ('close', 'Cerrado'),
        ('cancel', 'Cancelado'),
        ],default='draft')
    partner_id = fields.Many2one('res.partner', string='Transportista', required=True)

    fecha_de_salida = fields.Date(string="Fecha de salida", required=True)
    fecha_de_regreso = fields.Date(string="Fecha de regreso")
    facturas_ids = fields.One2many("transport.facturas","transporte_id",string="Facturas")
    ceompras_ids = fields.One2many("transport.ceompras","transporte_id",string="Compras")
    transferencias_ids = fields.One2many("transport.transferencias","transporte_id",string="Transferencias")

    @api.model
    def create(self,vals):
        if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('transporte') or _('New')
        result=super(Transporte,self).create(vals)
        return result
   
    def validar_nota(self):
        self.write({'state': 'valid'})
        return True

    def cerrar(self):
        self.write({'state': 'close'})
        for facturas in self.facturas_ids:
           if facturas.regreso == 'entregado':
              factura = self.env['account.invoice'].search([('id','=',facturas.folio.id)],limit=1)
              factura.write({'entregado': True})
        for compras in self.ceompras_ids:
           if compras.regreso == 'entregado':
              compra = self.env['purchase.order'].search([('id','=',compras.folio.id)],limit=1)
              compra.write({'entregado': True})
        for transferencias in self.transferencias_ids:
           if transferencias.regreso == 'entregado':
              tranferencia = self.env['stock.picking'].search([('id','=',transferencias.folio.id)],limit=1)
              tranferencia.write({'entregado': True})
        return True

    def cancelar(self):
        self.write({'state': 'cancel'})
        for facturas in self.facturas_ids:
           if facturas.regreso == 'entregado':
              factura = self.env['account.invoice'].search([('id','=',facturas.folio.id)],limit=1)
              factura.write({'entregado': False})
        for compras in self.ceompras_ids:
           if compras.regreso == 'entregado':
              compra = self.env['purchase.order'].search([('id','=',compras.folio.id)],limit=1)
              compra.write({'entregado': False})
        for transferencias in self.transferencias_ids:
           if transferencias.regreso == 'entregado':
              tranferencia = self.env['stock.picking'].search([('id','=',transferencias.folio.id)],limit=1)
              tranferencia.write({'entregado': False})
        return True

    @api.multi
    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")