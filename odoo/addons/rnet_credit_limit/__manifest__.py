{
    'name': "RNET - Credit Limit",
    'author': "RNET",
    'version': '0.1',

    'depends': ['customer_credit_management'],

    'data': [
        'views/res_config_settings_view.xml',
        'views/sale_credit_limit_warning.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}