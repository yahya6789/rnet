# -*- coding: utf-8 -*-
{
    'name': "Gut Asset",
    'author': "4Net Prima Solusi",
    'version': '0.1',

    'depends': ['hr','purchase','rnet_asset','rnet_project', 'rnet_purchase_requisition', 'rnet_purchase_report', 'rnet_inventory', 'purchase_discount'],

    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/receipt.xml',
        'views/resources.xml',
        'views/receipt_templates.xml',
        'views/account.xml',
        'views/product.xml',
        'report/external_layout_standard.xml',
        'views/stock.xml',
        'views/purchase_order.xml',
        'views/project_views.xml',
        'views/purchase_requisition_view.xml',
        'report/purchase_order_templates.xml',
        'views/purchase_order_history.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}