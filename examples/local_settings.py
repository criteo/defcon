"""Local settings."""
SECRET_KEY = 'cepowqjcenwqcnewqoinwqowq'
DEBUG = True

DEFCON_COMPONENTS = {
    'production': {
        'name': 'Production',
        'description': 'All the production perimeter.',
        'link': 'https://github.com/iksaif/defcon/wiki/production',
        'contact': 'escalation@iksaif.net',
        'plugins': {
            'static': {
                'statuses': {
                    'a4ce3a48-d3bc-4474-aaf3-52db3d3213f8': {
                        'defcon': 5,
                        'title': 'Test status',
                        'description': 'This is a test status.',
                        'metadata': '{"foo": "bar"}',
                        'link': 'http://githun.com/iksaif/defcon',
                        'time_start': '2017-04-18T08:24:21.920695Z',
                        'time_end': None,
                        'override': False,
                    },
                },
            },
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
