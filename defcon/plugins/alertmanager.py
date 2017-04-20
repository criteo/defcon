"""DefCon Prometheus Alertmanager plugin."""
import requests

from defcon.plugins import base


class AlertmanagerPlugin(base.Plugin):
    """DefCon Static plugin.

    Config:
    TODO
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(AlertmanagerPlugin, self).__init__(config)
        # TODO: Validate config is not None.

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
        api_url = self._config['api'] + '/alerts/groups'
        receiver = self._config.get('receiver', None)
        labels = self._config.get('labels', None)

        r = requests.get(api_url)
        # TODO: parse stuff an generate status
        # print (r.json())
        return {}
