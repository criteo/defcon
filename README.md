# defcon
defcon

## Plugins

See [plugins/README.md](plugins/README.md)

## Quickstart

```
./manage.py migrate
./manage.py migrate --syncdb
./manage.py createsuperuser
./manage.py runserver
cp examples/local_settings.py defcon/
./manage.py loadplugins
./manage.py loadcomponents
./manage.py runplugins
```
