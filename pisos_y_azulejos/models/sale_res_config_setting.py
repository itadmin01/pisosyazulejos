# -*- coding: utf-8 -*-
from odoo import models, fields,api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
      
    lista_precio = fields.Many2one('product.pricelist',string="Lista de precios para productos" ,config_parameter='pisos_y_azulejos.lista_precio')
    
class ProductProduct(models.Model): 
    _inherit ="product.product"
    
    @api.model
    def create_price_list(self):
        pricelist_id = self.env["ir.config_parameter"].sudo().get_param("pisos_y_azulejos.lista_precio")
        try:
            pricelist_id = eval(pricelist_id)
        except Exception:
            pricelist_id=None
        if pricelist_id :    
            for product in self.search([]):
                price = product.with_context(pricelist=pricelist_id).price
                product.write({'list_price':price})
        return
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.onchange('price_unit')
    def unit_price_not_change(self):
        if self.product_id:
            price = self.product_id.with_context(pricelist=self.order_id.pricelist_id.id).price
            if self.price_unit < price :
                self.price_unit=price
                #self.write({'price_unit' : price})
                
                
           
                