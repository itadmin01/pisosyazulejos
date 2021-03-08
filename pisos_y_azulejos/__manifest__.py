# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name':'Pisos y Azulejos',
    'version': '11.1',
    'summary':'Agrega modificaciones solicitadas por Pisos y Azulejos', 
    'category':"sale_order",
    'description' :'pisos_y_azulejos ',
    'depends':['sale','kanban_draggable'],
    'data':[
           'views/sale_res_config_setting.xml',
           'views/purchase_extends_form.xml',
           'views/inventory_kanban_edit.xml',
           'data/crone_data.xml',
        ],
}
