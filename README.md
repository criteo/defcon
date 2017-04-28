# DefCon

[![Build Status](https://travis-ci.org/iksaif/defcon.svg?branch=master)](https://travis-ci.org/iksaif/defcon)
[![Coverage Status](https://coveralls.io/repos/github/iksaif/defcon/badge.svg)](https://coveralls.io/github/iksaif/defcon?branch=master)
[![Dependency Status](https://gemnasium.com/badges/github.com/iksaif/defcon.svg)](https://gemnasium.com/github.com/iksaif/defcon)

UI and API to show an aggregate status of your services.

[![DefCon screenshot](doc/defcon.png)](doc/defcon.png)

*This is currently under active development and not ready for production.*

## API

Simply go to `/api/defcon/<COMPONENT_ID>/`.

```json
GET /api/defcon/observability/
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "url": "http://defcon/api/components/observability/",
    "plugins": [
        {
            "url": "http://defcon/api/plugin_instance/4/",
            "statuses": [],
            "name": "alertmanager-page",
            "config": "{'receiver': 'observability-page', 'defcon': 2, 'api': 'https://alertmanager/api/v1/'}",
            "plugin": "http://defcon/api/plugin/alertmanager/"
        },
        {
            "url": "http://defcon/api/plugin_instance/5/",
            "name": "alertmanager-ticket",
            "description": "",
            "config": "{'receiver': 'observability-ticket', 'defcon': 4, 'api': 'https://alertmanager/api/v1/'}",
            "plugin": "http://defcon/api/plugin/alertmanager/"
        }
    ],
    "statuses": [],
    "defcon": 5,
    "name": "Observability",
    "description": "",
    "link": "https://confluence/display/OBS",
    "contact": "observability@iksaif.net"
}
```

There are also more things available on `/api/`.

## Plugins

See [defcon/plugins/README.md](defcon/plugins/README.md)

## Quickstart

```
virtualenv venv -p python3
source venv/bin/activate
cp examples/local_settings.py defcon/
pip install -r requirements.txt
./manage.py migrate
./manage.py migrate --run-syncdb
./manage.py createsuperuser
./manage.py loadplugins
./manage.py loadcomponents
./manage.py runplugins
./manage.py runserver
```
