{
    'name': 'Amibara Performance Evaluation',
    'version': '16.1',
    'summary': 'Performance Amibara',
    'description': """Amibara""",
    'category': 'Human Resource',
    'website': '',
    'depends': [
        'base',
        'base_setup',
        'hr'
    ],

    'license': 'LGPL-3',

    'data': [

        'security/ir.model.access.csv',
        'views/employee_performance.xml',
        # 'views/manager_performance.xml',
        'data/data.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
