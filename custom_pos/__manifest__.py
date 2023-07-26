# -*- coding: utf-8 -*-
{
    'name': "Custom POS",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
 
    'assets': {
        'point_of_sale.assets': [
            'custom_pos/static/src/js/**.js',
            ],
        'web.assets_qweb': [
            'custom_pos/static/src/xml/pos.xml',
            'custom_pos/static/src/xml/cashnow.xml',
           ],

        }
}
