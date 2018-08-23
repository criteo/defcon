"""DefCon Prometheus Alertmanager plugin."""
import requests
import logging

from defcon.plugins import base


class EndpointPlugin(base.Plugin):
    """DefCon Endpoint plugin.

    set an endpoint to get a defcon level.
    The endpoint should have the info {...'defcon':[1-5],...}
    Another endPoint can be setup to force the level

    Config:
    ```python
    {
        'title': 'Defcon Production',
        'url': 'http://defcon.com/api/simple/production/', // Url to endpoint
        'link_status': 'http://defcon.com/status/production/ // Url to endpoint info
        'force_url': 'http://defcon.com/api/simple/force/, // Url to force endpoint
    }
    ```
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(EndpointPlugin, self).__init__(config)
        if config is None:
            config = {}

        self.url = config.get('url')
        self.force_url = config.get('force_url', 'http://defcon.com/status')
        self.title = config.get('title', '')
        self.link_status = config.get('link_status', '')

    @property
    def short_name(self):
        """Return the short name."""
        return 'endpoint'

    @property
    def name(self):
        """Return the name."""
        return 'endpoint'

    @property
    def description(self):
        """Return the description."""
        return 'Returns statuses based on endpoint.'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/iksaif/defcon'

    def _get_defcon_from_url(self, url):
        r = requests.get(self.url)
        r.raise_for_status()
        return (r.json().get('defcon', []))

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        if self._config is None:
            return ret

        defcon = 0

        if self.force_url is not None:
            try:
                defcon = self._get_defcon_from_url(self.force_url)
            except requests.exceptions.RequestException as e:
                print(e)
                defcon = 0
        if int(defcon) == 0:
            try:
                defcon = self._get_defcon_from_url(self.url)
            except requests.exceptions.RequestException as e:
                print(e)
                defcon = 5
            status = self._to_status(defcon, self.url)
            if status is not None:
                ret[status['id']] = status
        else:
            status = self._to_status(defcon, self.force_url)
            if status is not None:
                ret[status['id']] = status
        return ret

    def _to_status(self, defcon, url):
        """Return a status or None."""
        logging.debug('Handling %s' % (url))

        status = base.Status(
            title=self.title,
            link=self.link_status,
            defcon=defcon,
            description=self.description,
        )
        return status
