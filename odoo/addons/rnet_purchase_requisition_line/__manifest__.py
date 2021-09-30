{
    'name': "RNET - Purchase Requisition Line",
    'author': "RNET",
    'version': '0.1',

    'depends': ['rnet_purchase_requisition', 'rnet_purchase'],

    'data': [
        'views/purchase_requisition_line_view.xml',
        'security/ir.model.access.csv',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}