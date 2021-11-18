{
    'name': "RNET - Inventory",
    'author': "RNET",
    'version': '0.1',

    'depends': ['stock'],

    'data': [
        'security/ir.model.access.csv',
        'data/product_sequence.xml',
        'views/brand_view.xml',
        'views/product_group_views.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}