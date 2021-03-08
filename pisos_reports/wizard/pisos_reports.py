# -*- coding: utf-8 -*-#
from odoo import api, fields, models
import io
import xlwt
import itertools
import base64
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class PisosReport(models.TransientModel):
    _name = "pisos.report"
    
    date_start=fields.Date("Periodo")
    date_end= fields.Date('Al')
    partner_id = fields.Many2one('res.partner')
    report_data = fields.Binary('Report Data')
    documents = fields.Selection([('customer','Clientes'),('supplier','Proveedor')], string='Documentos', default='customer')
    monto_minimo =  fields.Float('Monto minimo', default=10)
    
    @api.multi
    def action_generate_xls_report(self):
        domain = [('date_invoice','>=',self.date_start),('date_invoice','<=',self.date_end),('state','=','open'),('type','=','out_invoice')]
        invoices = self.env['account.invoice'].search(domain)
        orders = invoices.mapped('invoice_line_ids').mapped('sale_line_ids').mapped('order_id')
        report_invoices = self.env['account.invoice'].browse()
        for order in orders:
            if order.picking_ids and list(set(order.picking_ids.mapped('state')))[0]=='done':
                report_invoices += order.invoice_ids

        final_records=[]
        for report_date in report_invoices:
            if report_date.type == 'out_invoice':
               praper_data={'Fecha':datetime.strftime(report_date.date_invoice,'%Y-%m-%d'),
                                'Nombre':report_date.partner_id.name,
                                'Vendedor':report_date.team_id.name,
                                'Documento':report_date.origin,
                                'Folio':report_date.number,
                                'Total':report_date.amount_total,
                                'Monto':report_date.residual}
               final_records.append(praper_data) 
        
             
        workbook = xlwt.Workbook()
        worksheet= workbook.add_sheet('Sheet 1')
        col_width = 256 * 22
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass
        style_name = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;')
        style = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;' "borders: top thin, bottom thin, left thin, right thin;")
        row = 0
        worksheet.row(row).height = 256 * 4
        worksheet.write(row,0,'Fecha',style)
        worksheet.write(row,1,'Nombre',style)
        worksheet.write(row,2,'Vendero',style)
        worksheet.write(row,3,'Documento Origen',style)
        worksheet.write(row,4,'Folio',style)
        worksheet.write(row,5,'Total',style)
        worksheet.write(row,6,'Monto adeudado',style)
        
        row += 1
        print (final_records)
        for invoice_data in final_records:
            worksheet.write(row,0,invoice_data['Fecha'])
            worksheet.write(row,1,invoice_data['Nombre'])
            worksheet.write(row,2,invoice_data['Vendedor'])
            worksheet.write(row,3,invoice_data['Documento'])
            worksheet.write(row,4,invoice_data['Folio'])
            worksheet.write(row,5,invoice_data['Total'])
            worksheet.write(row,6,invoice_data['Monto'])
            row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        self.write({'report_data':base64.b64encode(fp.getvalue())})
        return {
                'type' : 'ir.actions.act_url',
                'url': "/web/content/?model=pisos.report&id=" + str(self.id) + "&field=report_data&download=true&filename=Report Cliente.xls",
                'target':'self',
                }     
        
    
    @api.multi
    def action_generate_xls_report_no_entregadas(self):
        domain = [('date_invoice','>=',self.date_start),('date_invoice','<=',self.date_end),('state','not in',['draft','cancel'])]
        invoices = self.env['account.invoice'].search(domain)
        orders = invoices.mapped('invoice_line_ids').mapped('sale_line_ids').mapped('order_id')
        report_invoices = self.env['account.invoice'].browse()
        order_picking_dict={}
        for order in orders:
            if order.picking_ids and list(set(order.picking_ids.mapped('state')))[0]!='done':
                for invoice in order.invoice_ids:
                    order_picking_dict.update({invoice:order.picking_ids[0]})
                report_invoices += order.invoice_ids

        final_records=[]
        for invoice_data in report_invoices:
            picking=order_picking_dict.get(invoice)
            so_order = self.env['sale.order'].search([('name','=',invoice_data.origin)],limit=1)
            praper_data={'Fecha': so_order.commitment_date and datetime.strftime(so_order.commitment_date,'%Y-%m-%d') or '',
                                'Nombre':invoice_data.partner_id.name,
                                'Vendedor':invoice_data.team_id.name,
                                'Documento':invoice_data.origin,
                                'Folio':invoice_data.number,
                                'Incoterms':invoice_data.incoterm_id.name,
                                'Estado':picking.state,
                                'Total':invoice_data.amount_total,
                                'Monto':invoice_data.residual}
            final_records.append(praper_data) 
        
             
        workbook = xlwt.Workbook()
        worksheet= workbook.add_sheet('Sheet 1')
        col_width = 256 * 22
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass
        style_name = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;')
        style = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;' "borders: top thin, bottom thin, left thin, right thin;")
        row = 0
        worksheet.row(row).height = 256 * 4
        worksheet.write(row,0,'Fecha',style)
        worksheet.write(row,1,'Nombre',style)
        worksheet.write(row,2,'Vendero',style)
        worksheet.write(row,3,'Documento Origen',style)
        worksheet.write(row,4,'Folio',style)
        worksheet.write(row,5,'Incoterms',style)
        worksheet.write(row,6,'Estado',style)
        worksheet.write(row,7,'Total',style)
        worksheet.write(row,8,'Monto adeudado',style)
        
        row += 1
        print (final_records)
        for invoice_data in final_records:
            worksheet.write(row,0,invoice_data['Fecha'])
            worksheet.write(row,1,invoice_data['Nombre'])
            worksheet.write(row,2,invoice_data['Vendedor'])
            worksheet.write(row,3,invoice_data['Documento'])
            worksheet.write(row,4,invoice_data['Folio'])
            worksheet.write(row,5,invoice_data['Incoterms'])
            worksheet.write(row,6,invoice_data['Estado'])
            worksheet.write(row,7,invoice_data['Total'])
            worksheet.write(row,8,invoice_data['Monto'])
           
            row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        self.write({'report_data':base64.b64encode(fp.getvalue())})
        return {
                'type' : 'ir.actions.act_url',
                'url': "/web/content/?model=pisos.report&id=" + str(self.id) + "&field=report_data&download=true&filename=Report Cliente.xls",
                'target':'self',
                }     
    
    
    @api.multi
    def action_generate_xls_report_pagos_sin_aplicar_report(self):
#         domain = [('payment_date','>=',self.date_start),('payment_date','<=',self.date_end),('payment_type','=','inbound'),('move_reconciled','=','False'),('partner_id','!=','False')]
        domain = [('date','>=',self.date_start),('date','<=',self.date_end),('state','=','posted'),('journal_id.type','in',['bank', 'cash']),('matched_percentage', '<', '1')]
        #if self.partner_id:
        #    domain.append(('partner_id','=',self.partner_id.id))

        #if self.documents == 'customer':
        #    domain.append(('payment_type','=','inbound'))
        #else:
        #    domain.append(('payment_type','=','outbound'))

        #if self.documents:
        #    domain.append(('partner_type','=',self.documents))
        
        payments = self.env['account.move'].search(domain)
        workbook = xlwt.Workbook()
        worksheet= workbook.add_sheet('Sheet 1')
        col_width = 256 * 22
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass
        
        
        style_name = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;')
        style = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;' "borders: top thin, bottom thin, left thin, right thin;")
        row = 0
        worksheet.write(row,0,'Fecha',style)
        worksheet.write(row,1,'Apunte contable',style)
        worksheet.write(row,2,'Número',style)
        worksheet.write(row,3,'Empresa',style)
        worksheet.write(row,4,'Importe',style)
        worksheet.write(row,5,'% conciliado',style)
        worksheet.write(row,6,'Impote conciliado',style)
        worksheet.write(row,7,'Importe resultado',style)

        final_records=[]
        for payment in payments:
            _logger.info('pago %s ', payment.name)
            if payment.amount - payment.amount * payment.matched_percentage < self.monto_minimo:
                continue
            else:
                payment_data={'Fecha':datetime.strftime(payment.date,'%d-%m-%Y'),
                              'Apunte contable':payment.line_ids[0].name,
                              'Número': payment.name,
                              'Empresa': payment.partner_id.name,
                              'Importe': payment.amount,
                              '% conciliado': payment.matched_percentage,
                              'Impote conciliado': payment.amount * payment.matched_percentage,
                              'Importe resultado': payment.amount - payment.amount * payment.matched_percentage}
                final_records.append(payment_data)
       
        print (final_records)
        row += 1
        for invoice_data in final_records:
            worksheet.write(row,0,invoice_data['Fecha'])
            worksheet.write(row,1,invoice_data['Apunte contable'])
            worksheet.write(row,2,invoice_data['Número'])
            worksheet.write(row,3,invoice_data['Empresa'])
            worksheet.write(row,4,invoice_data['Importe'])
            worksheet.write(row,5,invoice_data['% conciliado'])
            worksheet.write(row,6,invoice_data['Impote conciliado'])
            worksheet.write(row,7,invoice_data['Importe resultado'])
            row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        self.write({'report_data':base64.b64encode(fp.getvalue())})
        return {
                'type' : 'ir.actions.act_url',
                'url': "/web/content/?model=pisos.report&id=" + str(self.id) + "&field=report_data&download=true&filename=Report Cliente.xls",
                'target':'self',
                }     
        
        