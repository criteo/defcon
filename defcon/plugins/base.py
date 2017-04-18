"""API to create plugins and some utilities."""
import abc


class Plugin(object):
    """Abstract class for plugins."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        """Create the plugin instance.

        Args:
          config: dict(string, any)
        """
        self._config = config

    @abc.abstractproperty
    def short_name(self):
        """Return the short_name of the plugin.

        It must contain only alphanumeric characters.
        """
        return None

    @abc.abstractproperty
    def name(self):
        """Return the name of the plugin."""
        return None

    @property
    def description(self):
        """Return a description."""
        return None

    @property
    def link(self):
        """Return a link."""
        return None

    @abc.abstractmethod
    def statuses(self):
        """Return a list of statuses.

        Returns:
          iterable(defcon.models.Status).
        """
        return {}
