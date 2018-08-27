"""Test endpoint."""
import httmock
import os

from django import test

from defcon.plugins import endpoint


@httmock.urlmatch()
def _endpoint_mock(url, request):
    if url.netloc == "foo.endpoint.io":
        filename = 'spec_endpoint_fields.json'
    else:
        filename = 'spec_endpoint_err.json'
    filename = os.path.join(
        os.path.dirname(__file__),
        filename
    )
    return open(filename).read()


class EndPointPluginTests(test.TestCase):
    """Test the plugins."""

    _API_URLS_OK = [
        'http://foo.endpoint.io/api/bar/',
    ]
    _API_URLS_NO_INFOS = [
        'http://bar.endpoint.io/',
    ]

    def test_base(self):
        """Basic test."""
        p = endpoint.EndpointPlugin()
        self.assertFalse(p.statuses())

    def test_ok(self):
        """Test with some settings."""
        for api_url in self._API_URLS_OK:
            with httmock.HTTMock(_endpoint_mock):
                p = endpoint.EndpointPlugin(
                    {
                        'url': api_url,
                    }
                )
                statuses = sorted(p.statuses().values())
                status = statuses[0]

                self.assertEqual(status['defcon'], 5)
                self.assertEqual(status['title'], 'Test')
                self.assertEqual(status['description'], 'foo')

    def test_no_infos(self):
        """Test with some settings."""
        for api_url in self._API_URLS_NO_INFOS:
            with httmock.HTTMock(_endpoint_mock):
                p = endpoint.EndpointPlugin(
                    {
                        'url': api_url,
                    }
                )
                statuses = sorted(p.statuses().values())
                status = statuses[0]

                self.assertEqual(status['defcon'], 5)
                self.assertEqual(
                    status['title'], "name not found from {}".format(api_url))
                self.assertEqual(
                    status['description'], "description not found from {}".format(api_url))
