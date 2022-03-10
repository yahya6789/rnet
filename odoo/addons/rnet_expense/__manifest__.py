{
    'name': "RNET - Expenses",
    'author': "RNET",
    'version': '0.1',

    'depends': ['hr_expense','hr_expense_request_advance'],

    'data': [
        'security/ir.model.access.csv',
        'views/expense.xml',
        'views/partner_view.xml',
        'report/expense.xml',
        'wizard/hr_expense_advance_register_payment.xml',
        #
        'views/sequence.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}