"""DefCon Prometheus Jira plugin."""
from __future__ import absolute_import

import logging
import jinja2
import jira

from defcon.plugins import base


class JiraPlugin(base.Plugin):
    """DefCon Static plugin.

    Config:
    ```python
    {
      'url': 'http://jira', // Url to root API.
      'username': 'foo',
      'password': 'bar',
      'jql': {},            // Get tickets matching this jql.
      'max_results': 5,
      'title_template': '{{ labels.alertname }}',
      'description_template': '{{ annotations }}',
      'link_template': '{{ me }}',
      'defcon': callback or int, // raw int or callback returning defcon
    }
    ```
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(JiraPlugin, self).__init__(config)
        if config is None:
            config = {}

        self.title_template = config.get(
            'title_template', '{{ key }} - {{ fields.summary }}'
        )
        self.description_template = config.get(
            'description_template',
            '{{ fields.description }}'
        )
        self.link_template = config.get(
            'link_template', '{{ permalink }}')
        self.receiver = config.get('receiver', None)
        self.labels = config.get('labels', None)
        self.max_results = config.get('max_results', 5)

        if config:
            self.url = config['url']
            self.username = config['username']
            self.password = config['password']
            self.defcon = config['defcon']
            self.jql = config['jql']

    @property
    def short_name(self):
        """Return the short name."""
        return 'jira'

    @property
    def name(self):
        """Return the name."""
        return 'Jira'

    @property
    def description(self):
        """Return the description."""
        return 'Returns statuses based on alerts on jira.'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/iksaif/defcon'

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        if self._config is None:
            return ret

        basic_auth = (self.username, self.password)
        client = jira.JIRA(self.url, basic_auth=basic_auth, timeout=5)

        issues = client.search_issues(self.jql, maxResults=self.max_results)
        for issue in issues:
            status = self._to_status(issue)
            if status is not None:
                ret[status['id']] = status
        return ret

    @staticmethod
    def render(template, data):
        """Render a string as a template."""
        env = jinja2.Environment()
        return env.from_string(template).render(**data)

    def _to_status(self, issue):
        """Return a status or None."""
        logging.debug('Handling %s' % (issue.fields.summary))

        # Guess the level.
        if callable(self.defcon):
            defcon = self.defcon(issue)
        else:
            defcon = self.defcon

        data = dict(issue.raw)
        data['me'] = data['self']
        data['issue'] = issue
        data['permalink'] = issue.permalink()
        del data['self']
        status = base.Status(
            self.render(self.title_template, data),
            defcon,
            self.render(self.link_template, data),
            description=self.render(self.description_template, data),
            # TODO: use some custom fields for dates.
            # time_start=dateparse.parse_datetime(alert['startsAt']),
            # time_end=dateparse.parse_datetime(alert['endsAt']),

        )
        return status
