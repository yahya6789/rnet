# -*- coding: utf-8 -*-
{
    'name': "WBN",
    'author': "4Net Prima Solusi",
    'website': "",

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': ['base', 'sale', 'rnet_purchase', 'stock', 'delivery'],

    'data': [
        'views/accounting.xml',
        'views/saleslines.xml',
        'views/purchaselines.xml',
        'views/resources.xml',
        'views/salesorder.xml',
        'views/quotations.xml',
        'views/invoice.xml',
        'views/expense.xml',
        'views/partner.xml',
        'views/partner-sequence.xml',
        'views/product_template_views.xml',
        'views/sale_views.xml',
        'views/business_unit_view.xml',
        'views/sales_area_view.xml',
        'views/product_views.xml',
        'security/ir.model.access.csv',
        'report/SalesReport.xml'
    ],

    'demo': [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}