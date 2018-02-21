"""DefCon Static plugin."""
import datetime
from defcon.plugins import base


class DaysHoursPlugin(base.Plugin):
    """DefCon Dayshours plugin.

    Config:

    ```python
    {
      'days': [0,1,2,3,4], // List of Int to specify day rule : if x is in days (Monday being 0 and Sunday being 6)
      'hours': [9,12], // Tuple of Int to specify hours rule : hours[0] < x < hours[1]
      'defcon' : 1, // Int to use as defcon
    }
    ```
    """

    def __init__(self, config=None):
        """Create an instance of the plugin."""
        super(DaysHoursPlugin, self).__init__(config)

        if config:
          self.days = config['days']
          self.hours = config['hours']
          self.defcon = config['defcon']

    @property
    def short_name(self):
        """Return the short name."""
        return 'dayshours'

    @property
    def name(self):
        """Return the name."""
        return 'Days and Hours'

    @property
    def description(self):
        """Return the description."""
        return 'Returns defcon if outside of days or hours'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/iksaif/defcon'

    def statuses(self):
        """Return the generated statuses."""
        ret = {}

        now = datetime.datetime.now()
        day = now.weekday()
        hour = now.hour
        if hour < self.hours[0] or hour > self.hours[1] or day not in self.days:
          status = base.Status(
            title="days/hours",
            defcon=self.defcon,
            link="",
            description="Current hour/day : {0}/{1} is out of day/hours rules".format(hour, day))
          if status is not None:
            ret[status['id']] = status

        return ret
