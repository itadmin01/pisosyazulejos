# -*- coding: utf-8 -*-#

from odoo import fields,api,models
import io
import xlwt
import base64

class TransporteRelacion(models.TransientModel):
    _name = "transporte.relacion"
    
    date_start=fields.Date("Periodo")
    date_end= fields.Date('Al')
    report_data = fields.Binary('Report Data')
    
    @api.multi
    def action_generate_xls_report(self):
        domain = [('fecha_de_regreso','>=',self.date_start),('fecha_de_regreso','<=',self.date_end),('state','in', ['valid','close'])]
        transportes = self.env['transporte'].search(domain)
        partner_wise_reocrd = {}
        for record in transportes:
            if record.partner_id not in partner_wise_reocrd:
                partner_wise_reocrd[record.partner_id] = []
            partner_wise_reocrd[record.partner_id].append(record)
             
        workbook = xlwt.Workbook()
        worksheet= workbook.add_sheet('Sheet 1')
#         worksheet.row(0).height = 256 * 2
#         worksheet.row(1).height = 256 * 4
        """col_width = 256 * 22
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass"""
#         style = xlwt.easyxf('pattern: pattern solid, fore_colour lime','font: bold True, color black, name Arial;')
        
        style_bold = xlwt.easyxf('font: bold True, color black')
        style = xlwt.easyxf('font: height 200, name Arial Black, bold on; align: wrap on, vert centre, horiz center;' "borders: top thin, bottom thin, left thin, right thin;")
        row = 0
        
        worksheet.row(row).height = 256 * 4
        worksheet.write(row,0,'Folio',style)
        worksheet.write(row,1,'Fecha de regreso',style)
        worksheet.write(row,2,'Transportista',style)
        worksheet.write(row,3,'Documento',style)
        worksheet.write(row,4,'Folio',style)
        worksheet.write(row,5,'Saldo cobrado',style)
        worksheet.write(row,6,'Regreso',style)
        worksheet.write(row,7,'Observaciones',style)
        worksheet.write(row,8,'Volumen',style)
        worksheet.write(row,9,'Precio',style)
        worksheet.write(row,10,'Flete',style)
        row += 1
        
        regreso = {'entregado': 'Entregado','devuelto' : 'Devuelto', 'entrega_parcial' : 'Entrega Parcial'}
        for partner, records in partner_wise_reocrd.items():
            total_saldo_cobrado = 0.0 
            total_volumen = 0.0
            total_precio = 0.0
            total_flete = 0.0
            
            for transporte in records:
                for line in transporte.facturas_ids:
                    worksheet.write(row,0,transporte.name)
                    worksheet.write(row,1,transporte.fecha_de_regreso)
                    worksheet.write(row,2,partner.name)
                    worksheet.write(row,3,'Factura')
                    worksheet.write(row,4,line.folio.number or '')
                    worksheet.write(row,5,line.saldo_cobrado)
                    worksheet.write(row,6,regreso.get(line.regreso,''))
                    worksheet.write(row,7,line.observaciones)
                    worksheet.write(row,8,line.volumen)
                    worksheet.write(row,9,line.precio or '')
                    worksheet.write(row,10,line.flete)
                    
                    total_saldo_cobrado += line.saldo_cobrado
                    total_volumen += line.volumen
                    total_precio += line.precio
                    total_flete += line.flete
                    
                    if row==1:
                        worksheet.set_panes_frozen(True)
                        worksheet.set_horz_split_pos(1)
                        worksheet.set_remove_splits(True)
                    row += 1
                    
                for line in transporte.ceompras_ids:
                    worksheet.write(row,0,transporte.name)
                    worksheet.write(row,1,transporte.fecha_de_regreso)
                    worksheet.write(row,2,partner.name)
                    worksheet.write(row,3,'Compras')
                    worksheet.write(row,4,line.folio.name or '')
                    worksheet.write(row,5,'')
                    worksheet.write(row,6,regreso.get(line.regreso,''))
                    worksheet.write(row,7,line.observaciones)
                    worksheet.write(row,8,line.volumen)
                    worksheet.write(row,9,line.precio or '')
                    worksheet.write(row,10,line.flete)
                    
                    #total_saldo_cobrado += line.saldo_cobrado
                    total_volumen += line.volumen
                    total_precio += line.precio
                    total_flete += line.flete
                    
                    if row==1:
                        worksheet.set_panes_frozen(True)
                        worksheet.set_horz_split_pos(1)
                        worksheet.set_remove_splits(True)
                    row += 1
                
                for line in transporte.transferencias_ids:
                    worksheet.write(row,0,transporte.name)
                    worksheet.write(row,1,transporte.fecha_de_regreso)
                    worksheet.write(row,2,partner.name)
                    worksheet.write(row,3,'Transferencia')
                    worksheet.write(row,4,line.folio.name or '')
                    worksheet.write(row,5,'')
                    worksheet.write(row,6,regreso.get(line.regreso,''))
                    worksheet.write(row,7,line.observaciones)
                    worksheet.write(row,8,line.volumen)
                    worksheet.write(row,9,line.precio or '')
                    worksheet.write(row,10,line.flete)
                    
                    #total_saldo_cobrado += line.saldo_cobrado
                    total_volumen += line.volumen
                    total_precio += line.precio
                    total_flete += line.flete
                    
                    if row==1:
                        worksheet.set_panes_frozen(True)
                        worksheet.set_horz_split_pos(1)
                        worksheet.set_remove_splits(True)
                    row += 1
            
            #Add Full total for Column 5,8,9 and 10
            worksheet.write(row,0,'')
            worksheet.write(row,1,'')
            worksheet.write(row,2,'')
            worksheet.write(row,3,'')
            worksheet.write(row,4,'')
            worksheet.write(row,5,total_saldo_cobrado,style_bold)
            worksheet.write(row,6,'')
            worksheet.write(row,7,'')
            worksheet.write(row,8,total_volumen,style_bold)
            worksheet.write(row,9,total_precio,style_bold)
            worksheet.write(row,10,total_flete,style_bold)
                                
            row += 2
        
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        self.write({'report_data':base64.b64encode(fp.getvalue())})
        return {
                'type' : 'ir.actions.act_url',
                'url': "/web/content/?model=transporte.relacion&id=" + str(self.id) + "&field=report_data&download=true&filename=Transporte Relacion.xls",
                'target':'self',
                }   