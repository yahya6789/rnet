# -*- coding: utf-8 -*-
{
    'name': "Gut Asset",
    'author': "4Net Prima Solusi",
    'version': '0.1',

    'depends': ['hr','rnet_asset','rnet_purchase_requisition'],

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
        'views/purchase_requisition_view.xml'
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}