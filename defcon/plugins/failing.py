"""DefCon Failing plugin."""
from defcon.plugins import base


class FailingPlugin(base.Plugin):
    """DefCon Failing plugin.

    Config:
    * statuses: dict(uuid -> status)

    Example:
    ```python
     {
       'statuses': {
         'a4ce3a48-d3bc-4474-aaf3-52db3d3213f8' : {
           'title': 'Fail status'
        },
      },
    }
    ```

    You can also use defcon.plugins.base.Status.
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(FailingPlugin, self).__init__(config)

    @property
    def short_name(self):
        """Return the short name."""
        return 'failing'

    @property
    def name(self):
        """Return the name."""
        return 'Failing'

    @property
    def description(self):
        """Return the description."""
        return 'Raise an exception returning statuses'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/criteo/defcon'

    def statuses(self):
        """Return the generated statuses."""
        raise Exception("Failed to generate statuses")
