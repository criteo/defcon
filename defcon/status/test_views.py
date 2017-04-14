from django import test

from defcon.status import views

class ViewTestcase(test.TestCase):
    def test_component_view_set(self):
        views.ComponentViewSet()
