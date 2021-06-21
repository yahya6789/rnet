{
    'name': "RNET - MRP",
    'author': "RNET",
    'version': '0.1',

    'depends': ['mrp'],

    'data': [
        'security/ir.model.access.csv',
        'views/mrp.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}