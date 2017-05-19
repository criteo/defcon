"""DefCon Prometheus Alertmanager plugin."""
import requests
import logging
import jinja2

from django.utils import dateparse
from defcon.plugins import base


class AlertmanagerPlugin(base.Plugin):
    """DefCon Static plugin.

    Config:
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
            self.api_url = config['api'] + '/alerts/groups'
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
        return 'https://github.com/iksaif/defcon'

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        if self._config is None:
            return ret

        r = requests.get(self.api_url)
        # TODO: parse stuff an generate status
        data = r.json().get('data', [])
        for root_alert in data:
            blocks = root_alert.get('blocks', []) or []
            for block in blocks:
                alerts = block.get('alerts', []) or []
                for alert in alerts:
                    status = self._to_status(root_alert, block, alert)
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

    def _to_status(self, root_alert, block, alert):
        """Return a status or None."""
        logging.debug('Handling %s' % (alert))
        if not self.match_labels(root_alert['labels'], self.labels):
            return None
        if not self.match_labels(alert['labels'], self.labels):
            return None
        if self.receiver is not None:
            if block['routeOpts']['receiver'] != self.receiver:
                return None
        if alert.get('inhibited') or alert.get('silenced'):
            logging.debug('alert is inactived')
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
