{
    'name': "RNET - Inventory",
    'author': "RNET",
    'version': '0.1',

    'depends': ['stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/brand_view.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}