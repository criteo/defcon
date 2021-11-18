"""DefCon Prometheus Alertmanager plugin."""
import requests
import logging
import jinja2

from django.utils import dateparse
from django.conf import settings
from defcon.plugins import base


DEFAULT_API = getattr(settings, 'ALERTMANAGER_API', None)
DEFAULT_API_PROXIES = getattr(settings, 'ALERTMANAGER_API_PROXIES', None)
DEFAULT_API_USERNAME = getattr(settings, 'ALERTMANAGER_API_USERNAME', None)
DEFAULT_API_PASSWORD = getattr(settings, 'ALERTMANAGER_API_PASSWORD', None)


class AlertmanagerPlugin(base.Plugin):
    """DefCon Static plugin.

    Config:
    ```python
    {
      'api': 'http://alertmanager:9090/api/v2', // Url to root API.
      'api_username': None,
      'api_password': None,
      'receiver': 'default', // Get alerts rooted to this receiver.
      'labels': {}, // Get alerts matching these labels.
      'title_template': '{{ labels.alertname }}',
      'description_template': '{{ annotations }}',
      'link_template': '{{ generatorURL }}',
      'defcon': 'label' or int, // Label to use as defcon or raw int.
    }
    ```
    Alert ex:
    # {
    #     "alerts": [
    #     {
    #         "annotations": {
    #         "description": "Local instance is not responding for more than 20 minutes.",
    #         "documentation": "https://example.com",
    #         "summary": "down in dc2"
    #         },
    #         "endsAt": "2019-08-23T12:47:48.736Z",
    #         "fingerprint": "65QSDFJHKsdjqnsdqsjkhd9",
    #         "receivers": [{ "name": "default" }, { "name": "logs" }],
    #         "startsAt": "2019-08-23T12:44:48.736Z",
    #         "status": { "inhibitedBy": [], "silencedBy": [], "state": "active" },
    #         "updatedAt": "2019-08-23T12:44:48.813Z",
    #         "generatorURL": "http://prometheus-example",
    #         "labels": {
    #         "alertname": "LocalDown",
    #         "dc": "sdc2",
    #         "env": "prod",
    #         "level": "local",
    #         "perimeter": "mail",
    #         "severity": "page"
    #         }
    #     }
    #     ],
    #     "labels": {},
    #     "receiver": { "name": "teamName-slack" }
    # }
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(AlertmanagerPlugin, self).__init__(config)
        if config is None:
            config = {}

        self.title_template = config.get(
            'title_template', '{{ labels.alertname }}'
        )
        self.description_template = config.get(
            'description_template',
            'Labels: {{ labels }}\nAnnotations: {{ annotations }}'
        )
        self.link_template = config.get(
            'link_template', '{{ generatorURL }}')
        self.receiver = config.get('receiver', None)
        self.labels = config.get('labels', None)

        if config:
            self.api_url = config.get('api', DEFAULT_API) + '/api/v2/alerts/groups'
            self.api_proxies = config.get('api_proxies', DEFAULT_API_PROXIES)
            self.api_username = config.get('api_username', DEFAULT_API_USERNAME)
            self.api_password = config.get('api_password', DEFAULT_API_PASSWORD)
            self.defcon = config['defcon']

    @property
    def short_name(self):
        """Return the short name."""
        return 'alertmanager'

    @property
    def name(self):
        """Return the name."""
        return 'Alertmanager'

    @property
    def description(self):
        """Return the description."""
        return 'Returns statuses based on alerts on alertmanager.'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/criteo/defcon'

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        if self._config is None:
            return ret

        auth = (self.api_username, self.api_password)
        r = requests.get(self.api_url, auth=auth, proxies=self.api_proxies)
        r.raise_for_status()
        dataFull = r.json()
        for data in dataFull:
            alerts = data.get('alerts', []) or []
            for alert in alerts:
                status = self._to_status(alert)
                if status is not None:
                    ret[status['id']] = status
        return ret

    @staticmethod
    def match_labels(labels, needed_labels):
        """Return True if labels matche needed_labels."""
        logging.debug('Checking is %s matches %s' % (labels, needed_labels))
        if needed_labels is None:
            return True
        for k, v in needed_labels.items():
            if labels.get(k) != v:
                return False
            # TODO: handle regexp.
        return True

    @staticmethod
    def render(template, data):
        """Render a string as a template."""
        env = jinja2.Environment()
        return env.from_string(template).render(**data)

    def _to_status(self, alert):
        """Return a status or None."""
        logging.debug('Handling %s' % (alert))
        if not self.match_labels(alert['labels'], self.labels):
            return None
        status = alert.get('status', {})

        # Check Receiver
        if self.receiver is not None:
            if alert.get('receivers') is not None:
                receiverList = []
                for receveir in alert.get("receivers"):
                    if receveir["name"] is not None:
                        receiverList.append(receveir["name"])
                if self.receiver not in receiverList:
                    return None

        # Old API
        if alert.get('inhibited') or alert.get('silenced'):
            logging.debug('alert is inactive')
            return None
        # New API
        if status.get('state', 'active') != 'active':
            logging.debug('alert is inactived: %s' % status)
            return None

        # Guess the level.
        if type(self.defcon) == int:
            defcon = self.defcon
        elif callable(self.defcon):
            defcon = self.defcon(alert)
        else:
            defcon = int(alert['labels'][self.defcon])

        status = base.Status(
            self.render(self.title_template, alert),
            defcon,
            self.render(self.link_template, alert),
            description=self.render(self.description_template, alert),
            time_start=dateparse.parse_datetime(alert['startsAt']),
            time_end=dateparse.parse_datetime(alert['endsAt']),
        )
        return status
