"""Local settings."""
from defcon.plugins import base


SECRET_KEY = 'cepowqjcenwqcnewqoinwqowq'
DEBUG = True

DEFCON_COMPONENTS = {
    'production': {
        'name': 'Production',
        'description': 'All the production perimeter.',
        'link': 'https://github.com/iksaif/defcon/wiki/production',
        'contact': 'escalation@iksaif.net',
        'plugins': {
            'static': [
                base.Status('Test status', 5, 'http://github.com/iksaif/defcon',
                            description='This is a test'),
            ]
        },
    },
    'observability': {
        'name': 'Observability',
        'description': '',
        'link': 'https://github.com/iksaif/defcon/wiki/observability',
        'contact': 'obs@iksaif.net',
        'plugins': {},
    },
    'storage': {
        'name': 'Storage',
        'description': 'Storage Chef Perimeter',
        'link': 'https://github.com/iksaif/defcon/wiki/storage',
        'contact': 'storage@iksaif.net',
        'plugins': {},
    },
}

DEFCON_PLUGINS = [
    'defcon.plugins.static.StaticPlugin',
]
