"""DefCon Static plugin."""
from defcon.plugins import base


class StaticPlugin(base.Plugin):
    """DefCon Static plugin.

    Config:
    * statuses: dict(uuid -> status)

    Example:
    ```python
     {
       'statuses': {
         'a4ce3a48-d3bc-4474-aaf3-52db3d3213f8' : {
           'defcon': 5,
           'title': 'Test status',
           'description': 'This is a test status.',
           'metadata': '{"foo": "bar"}',
           'link': 'http://githun.com/criteo/defcon',
           'time_start': '2017-04-18T08:24:21.920695Z',
           'time_end': None,
           'override': False,
        },
      },
    }
    ```

    You can also use defcon.plugins.base.Status.
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(StaticPlugin, self).__init__(config)

    @property
    def short_name(self):
        """Return the short name."""
        return 'static'

    @property
    def name(self):
        """Return the name."""
        return 'Static'

    @property
    def description(self):
        """Return the description."""
        return 'Returns statically configured statuses.'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/criteo/defcon'

    def statuses(self):
        """Return the generated statuses."""
        statuses = self._config.get('statuses', {})

        if not isinstance(statuses, dict):
            statuses = {status['id']: dict(status) for status in statuses}

        # Always return a copy to avoid mutations from the caller.
        return dict(statuses)
