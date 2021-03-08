# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name':'Reportes Pisos y Azulejos',
    'version': '11.16',
    'summary':'Reportes de facturas solicitados por Pisos y Azulejos', 
    'category':"Accounting",
    'description' :'Make a Report in account.invoice module in reports ',
    'depends':['account', 'stock', 'purchase',
               'product_weight_volume_docs','stock_picking_weight_volume_doc',
               'hr_expense','account'],
    'data':[
           'data/ir_sequence_number.xml',
           'security/ir.model.access.csv',
           'views/transporte_view.xml',
           'views/pisos_reports_view.xml',
           'views/account_invoice.xml',
           'views/hr_expenses_extends.xml',
           'views/res_config_settings_views.xml',
           'wizard/transporte_relacion_view.xml',
           'wizard/pagos_sin_aplicar_report.xml',
           'reports/expense_report.xml',
           'reports/expense_report_templates.xml',
           'reports/transporte_report_template.xml',
           'reports/transporte_report.xml',
           'reports/my_expenses_reports.xml',
           'reports/hide_invoice_no_payment.xml',
           'reports/invoice_report_document.xml',
        ],
}
