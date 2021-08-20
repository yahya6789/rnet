# -*- coding: utf-8 -*-
{
    'name': "RNET - Sale Report",
    'author': "4Net Prima Solusi",
    'website': "",

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'report/SalesReport.xml',
        'views/saleslines.xml',
    ],

    'demo': [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}