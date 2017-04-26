# DefCon

[![Build Status](https://travis-ci.org/iksaif/defcon.svg?branch=master)](https://travis-ci.org/iksaif/defcon)
[![Coverage Status](https://coveralls.io/repos/github/iksaif/defcon/badge.svg)](https://coveralls.io/github/iksaif/defcon?branch=master)
[![Dependency Status](https://gemnasium.com/badges/github.com/iksaif/defcon.svg)](https://gemnasium.com/github.com/iksaif/defcon)

UI and API to show an aggregate status of your services.

[![DefCon screenshot](doc/defcon.png)](doc/defcon.png)


## API

## Plugins

See [defcon/plugins/README.md](defcon/plugins/README.md)

## Quickstart

```
virtualenv venv -p python3
source venv/bin/activate
cp examples/local_settings.py defcon/
./manage.py migrate
./manage.py migrate --run-syncdb
./manage.py createsuperuser
./manage.py loadplugins
./manage.py loadcomponents
./manage.py runplugins
./manage.py runserver
```
