{
    'name': "RNET - Expenses",
    'author': "RNET",
    'version': '0.1',

    'depends': ['hr_expense'],

    'data': [
        'security/ir.model.access.csv',
        'views/expense.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}