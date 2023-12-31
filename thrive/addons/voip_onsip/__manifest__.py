# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': "VOIP OnSIP",

    'description': """
Module with the required configuration to connect to OnSIP.
    """,

    'category': 'Hidden',
    'version': '1.0',

    'depends': ['voip'],

    'data': [
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        ],
    'license': 'OEEL-1',
    'assets': {
        'mail.assets_messaging': [
            'voip_onsip/static/src/models/*.js',
        ],
        'web.assets_backend': [
            'voip_onsip/static/src/**/*',
        ],
    }
}
