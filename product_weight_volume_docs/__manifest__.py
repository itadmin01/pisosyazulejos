# -*- coding: utf-8 -*-
{
    'name': 'Product weight and volume on Documents',
    'version': '1.2',
    'category': 'Extra',
    'author': 'Carlos A. Garcia',
    'website': 'http://www.ikom.mx',
    'summary': 'Añade el peso y volumen del producto en vistas y documentos.',
    'description': """
* Agrega los campos al documento PDF del modelo.
* Añadidos campos adicionales al reporte PDF de la factura.
""",
    'depends': ['account',
                'cdfi_invoice',
                ],
    'data': [
            'views/invoice_view.xml',
            # 'views/sale_view.xml',
            'views/purchase_view.xml',
            'report/invoice_report.xml',
            # 'report/sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: