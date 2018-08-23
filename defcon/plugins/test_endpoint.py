"""Test endpoint."""
from django import test

from defcon.plugins import endpoint

class AlertmanagerPluginTests(test.TestCase):
    """Test the plugins."""

    _API_URLS = [
        'http://foo.endpoint.io/api/defcon/',
    ]

    def test_base(self):
        """Basic test."""
        p = endpoint.EndpointPlugin()
        self.assertFalse(p.statuses())

    def test_all(self):
        """Test with some settings."""
        for api_url in self._API_URLS:
            p = endpoint.EndpointPlugin(
                {
                    'url': api_url,
                }
            )
            statuses = sorted(p.statuses().values())
            status = statuses[0]

            self.assertEqual(status['title'], '')
            self.assertEqual(status['defcon'], 5)
