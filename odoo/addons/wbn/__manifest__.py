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
        'views/resources.xml',
        'views/invoice.xml',
        'views/expense.xml',
        'views/partner.xml',
        'views/partner-sequence.xml',
        'views/product_template_views.xml',
        'views/business_unit_view.xml',
        'views/sales_area_view.xml',
        'views/product_views.xml',
        'views/product_group_views.xml',
        'security/ir.model.access.csv',
    ],

    'demo': [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}