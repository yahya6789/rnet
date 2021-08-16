{
    'name': "RNET - Asset",
    'author': "RNET",
    'version': '0.1',

    'depends': ['odoo_account_asset_extend_ce','om_account_asset'],

    'data': [
        'data/asset.xml',
        'security/ir.model.access.csv',
        'views/asset.xml',
        'views/asset_transfer.xml',
        'views/asset_transfer_type.xml',
        'views/calibration.xml',
        'views/takeout.xml',
        'views/takeout_templates.xml',
        'report/asset.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}