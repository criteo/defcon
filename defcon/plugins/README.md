# Plugins

This is a list of plugins shipped with defcon.

## Static

Module: `defcon.plugins.static.StaticPlugin`

This is a very simple plugin to add static statuses in the database, useuful
for scheduled events.

### Settings

Simply add a dict of statuses. Each must have its own unique uuid.

```python
{
  'statuses': {
    'a4ce3a48-d3bc-4474-aaf3-52db3d3213f8' : {
      'defcon': 5,
      'title': 'Test status',
      'description': 'This is a test status.',
      'metadata': '{"foo": "bar"}',
      'link': 'http://github.com/iksaif/defcon',
      'time_start': '2017-04-18T08:24:21.920695Z',
      'time_end': None,
      'override': False,
   },
 },
}
```

## OpsGenie

TBD

## Jira

Module: `defcon.plugins.jira.JiraPlugin`

```python
{
  'url': 'http://jira', // Url to root API.
  'username': 'foo',
  'password': 'bar',
  'jql': {},            // Get tickets matching this jql.
  'max_results': 5,
  'title_template': '{{ labels.alertname }}',
  'description_template': '{{ annotations }}',
  'link_template': '{{ generatorURL }}',
  'defcon': callback or int, // raw int or callback returning defcon
}
```

## Prometeus Alertmanager

Module: `defcon.plugins.alertmanager.AlertmanagerPlugin`

To be used to set defcon based on alerts.

## Static

```python
{
  'api': 'http://alertmanager:9090/api/v1', // Url to root API.
  'receiver': 'default', // Get alerts rooted to this receiver.
  'labels': {}, // Get alerts matching these labels.
  'title_template': '{{ labels.alertname }}',
  'description_template': '{{ annotations }}',
  'link_template': '{{ generatorURL }}',
  'defcon': 'label' or int, // Label to use as defcon or raw int.
}
```

## Write you own plugin.

Take a look at [static.py](static.py), basically you need to implement the `statuses` method of a `Plugin` sub-class to make it return a list of status based on the settings you receive.