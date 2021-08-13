# -*- coding: utf-8 -*-
{
    'name': "Gut Asset",
    'author': "4Net Prima Solusi",
    'version': '0.1',

    'depends': ['hr','rnet_asset'],

    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/receipt.xml',
        'views/resources.xml',
        'views/receipt_templates.xml',
        'views/account.xml',
        'views/purchase_order.xml',
        'views/product.xml',
        'report/asset.xml',
        'report/purchase_line.xml',
        'report/external_layout_standard.xml',
        'views/stock.xml',
        'views/purchase_requisition_view.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}