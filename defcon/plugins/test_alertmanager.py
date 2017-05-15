"""Test alertmanager."""
import httmock
import os

from django import test

from defcon.plugins import alertmanager


@httmock.urlmatch(netloc=r'(.*\.)?alertmanager\.io$')
def _alertmanager_mock(url, request):
    filename = os.path.join(
        os.path.dirname(__file__),
        'spec_alertmanager.json')
    return open(filename).read()


class AlertmanagerPluginTests(test.TestCase):
    """Test the plugins."""

    _API_URL = 'http://foo.alertmanager.io/api/v1/'

    def test_base(self):
        """Basic test."""
        p = alertmanager.AlertmanagerPlugin()
        self.assertFalse(p.statuses())

    def test_all(self):
        """Test with some settings."""
        with httmock.HTTMock(_alertmanager_mock):
            p = alertmanager.AlertmanagerPlugin(
                {
                    'api': self._API_URL,
                    'defcon': lambda _: 3,
                    'receiver': 'default',
                }
            )
            statuses = sorted(p.statuses().values())
            status = statuses[0]

            self.assertEqual(status['title'], 'ExampleAlertAlwaysFiring')
            self.assertEqual(status['defcon'], 3)

    def test_match_labels(self):
        """Check that we match labels properly."""
        p = alertmanager.AlertmanagerPlugin()

        labels = {'foo': 'bar', 'bar': 'foo'}
        self.assertTrue(p.match_labels(labels, {}))

        self.assertTrue(p.match_labels(labels, {'foo': 'bar'}))
        self.assertFalse(p.match_labels(labels, {'foo': 'foo'}))
