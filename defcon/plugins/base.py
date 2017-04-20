"""API to create plugins and some utilities."""
import abc
import uuid


class Status(dict):
    """Simple class to create statuses."""

    NAMESPACE = uuid.UUID('{656cf8aa-25bd-11e7-a9eb-68f7288416b6}')

    def __init__(self, title, defcon, link, id=None, description=None,
                 time_start=None, time_end=None, override=None):
        """Initialize a status."""
        s = self

        if id is not None and type(id) != uuid.UUID:
            id = uuid.uuid5(self.NAMESPACE, id)
        s['id'] = id or uuid.uuid5(uuid.NAMESPACE_URL, link)
        s['title'] = title
        s['link'] = link
        s['defcon'] = int(defcon)
        if description is not None:
            s['description'] = description
        if time_start is not None:
            s['time_start'] = time_start
        if time_end is not None:
            s['time_end'] = time_end
        if override is not None:
            s['override'] = override


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
          dict(uuid.UUID: defcon.plugins.base.Status).
        """
        return {}
