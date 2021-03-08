# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import pytz
from .tzlocal import get_localzone
from odoo import tools
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fecha_compromiso = fields.Datetime(string=_('Fecha Compromiso'), compute='_correct_commitment_date')

    def _correct_commitment_date(self):
        for invoice in self:
           if invoice.commitment_date:
              sale_order = invoice.env['sale.order'].search([('name','=',invoice.origin)],limit=1)
              invoice.fecha_compromiso = sale_order.commitment_date
           #corregir hora
  #         _logger.info('corregir fecha ... %s', fecha_mal)
   #        timezone = self._context.get('tz')
    #       if not timezone:
     #          timezone = self.env.user.partner_id.tz or 'America/Mexico_City'
      
 #          local = pytz.timezone(timezone)
  #         naive_from = fecha_mal
   #        local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
    #       self.fecha_compromiso = local_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
     #      _logger.info('fecha corregida... %s', self.commitment_date)
		   
		   