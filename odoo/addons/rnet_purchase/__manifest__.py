{
    'name': "RNET - Purchase",
    'author': "RNET",
    'version': '0.1',

    'depends': ['purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/vendor_category.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}