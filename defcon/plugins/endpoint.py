"""DefCon Endpoint plugin."""
import requests
import logging

from defcon.plugins import base


class EndpointPlugin(base.Plugin):
    """DefCon Endpoint plugin.

    Set an endpoint to get a defcon level.
    The endpoint should have the info {...'defcon':[1-5],...}

    Config:
    ```python
    {
        'url': 'http://defcon.com/api/simple/production/', // Url to endpoint
    }
    ```
    response from the url should be like the DefCon simple API:
    {
        "name": "Production",
        "contact": "production@prod.com",
        "link": "https://confluence/production+Home",
        "defcon": 3,
        "description": "fooo"
    }

    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(EndpointPlugin, self).__init__(config)
        if config is None:
            config = {}

        self.url = config.get('url')

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
        return 'https://github.com/criteo/defcon'

    def _get_defcon_from_url(self, url):
        r = requests.get(self.url)
        r.raise_for_status()
        return (r.json())

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        if self._config is None:
            return ret

        try:
            payload = self._get_defcon_from_url(self.url)

        except requests.exceptions.RequestException as e:
            # catch requests exceptions and create a false payload
            logging.exception(e)
            payload = {
                "name": "Failed to get info from {}".format(self.url),
                "contact": "Failed to get info from {}".format(self.url),
                "link": "Failed to get info from {}".format(self.url),
                "defcon": 5,
                "description": "Failed to get info from {}".format(self.url)
            }

        status = self._to_status(payload, self.url)

        if status is not None:
            ret[status['id']] = status
        return ret

    def _to_status(self, payload, url):
        """Return a status or None."""
        logging.debug('Handling %s' % (url))
        # if endpoint doesn't have all the infos
        # default message will be send
        status = base.Status(
            title=payload.get('name', "name not found from {}".format(url)),
            link=payload.get('link', "link not from {}".format(url)),
            defcon=payload.get('defcon', 5),
            description=payload.get('description', "description not found from {}".format(url)),
        )
        return status
