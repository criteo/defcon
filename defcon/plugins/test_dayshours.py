"""Test dayshours."""
import mock
import datetime

from django import test

from defcon.plugins import dayshours

class StubDate(datetime.datetime):
    pass

class DayshoursPluginTests(test.TestCase):

    def test_base(self):
        """Basic test."""
        p = dayshours.DayshoursPlugin()
        self.assertFalse(p.statuses())

    @mock.patch('defcon.plugins.dayshours.datetime.datetime', StubDate)
    def test_days(self):
        """Test with some settings."""
        from datetime import datetime
        """Mock time to a Friday 11am"""
        StubDate.now = classmethod(lambda cls: datetime(2018, 2, 23, 11, 00, 00, 00))

        p = dayshours.DayshoursPlugin(
            {
                'days': [0,1,2,3],
                'hours': [10,16],
                'defcon': 1,
            }
        )
        statuses = sorted(p.statuses().values())
        status = statuses[0]
        self.assertEqual(status['defcon'], 1)

    @mock.patch('defcon.plugins.dayshours.datetime.datetime', StubDate)
    def test_hours(self):
        """Test with some settings."""
        from datetime import datetime
        """Mock time to a Monday 9am"""
        StubDate.now = classmethod(lambda cls: datetime(2018, 2, 19, 9, 00, 00, 00))

        p = dayshours.DayshoursPlugin(
            {
                'days': [0,1,2,3],
                'hours': [10,16],
                'defcon': 1,
            }
        )
        statuses = sorted(p.statuses().values())
        status = statuses[0]
        self.assertEqual(status['defcon'], 1)
