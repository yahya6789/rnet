{
    'name': "RNET - Purchase Requisition",
    'author': "RNET",
    'version': '0.1',

    'depends': ['material_purchase_requisitions'],

    'data': [
        'views/purchase_requisition_view.xml',
        'report/requisition_template.xml',
        'report/purchase_requisition_template.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}