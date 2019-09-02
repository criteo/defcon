"""Test alertmanager."""
import httmock
import os

from django import test

from defcon.plugins import alertmanager


@httmock.urlmatch()
def _alertmanager_mock(url, request):
    if url.netloc == 'foo.alertmanager0.14.io':
        suffix = '_0.14'
    else:
        suffix = ''
    filename = os.path.join(
        os.path.dirname(__file__),
        'spec_alertmanager%s.json' % suffix
    )
    return open(filename).read()


class AlertmanagerPluginTests(test.TestCase):
    """Test the plugins."""

    _API_URLS = [
        'http://foo.alertmanager.io/',
    ]

    def test_base(self):
        """Basic test."""
        p = alertmanager.AlertmanagerPlugin()
        self.assertFalse(p.statuses())

    def test_all(self):
        """Test with some settings."""
        for api_url in self._API_URLS:
            with httmock.HTTMock(_alertmanager_mock):
                p = alertmanager.AlertmanagerPlugin(
                    {
                        'api': api_url,
                        'defcon': lambda _: 3,
                        'receiver': 'default',
                    }
                )
                statuses = sorted(p.statuses().values())
                status = statuses[0]

                self.assertEqual(status['title'], 'ExampleAlertAlwaysFiring')
                self.assertEqual(status['defcon'], 3)

                # statuses[1] have wrong receiver, so it should raise an exeption
                with self.assertRaises(IndexError):
                    statuses[1]

    def test_match_labels(self):
        """Check that we match labels properly."""
        p = alertmanager.AlertmanagerPlugin()

        labels = {'foo': 'bar', 'bar': 'foo'}
        self.assertTrue(p.match_labels(labels, {}))

        self.assertTrue(p.match_labels(labels, {'foo': 'bar'}))
        self.assertFalse(p.match_labels(labels, {'foo': 'foo'}))
