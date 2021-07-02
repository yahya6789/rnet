# -*- coding: utf-8 -*-
{
    'name': "WBN",
    'author': "4Net Prima Solusi",
    'website': "",

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': ['base', 'sale', 'purchase', 'stock', 'delivery'],

    'data': [
        'views/accounting.xml',
        'views/purchaseorder.xml',
        'views/saleslines.xml',
        'views/purchaselines.xml',
        'views/resources.xml',
        'views/salesorder.xml',
        'views/quotations.xml',
        'views/invoice.xml',
        'views/transfer.xml',
        'views/expense.xml',
        'views/partner.xml',
        'views/partner-sequence.xml',
        'views/stock_templates.xml',
        'security/ir.model.access.csv',
        'report/SalesReport.xml'
    ],

    'demo': [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}