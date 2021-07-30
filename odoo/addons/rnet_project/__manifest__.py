{
    'name': "RNET - Project",
    'author': "RNET",
    'version': '0.1',

    'depends': ['project'],

    'data': [
        'security/ir.model.access.csv',
        'data/project.xml',
        'views/project_views.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}