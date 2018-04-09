"""Urls for defcon.status."""
from django.conf.urls import include, url

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from defcon.status import views
# pylama:ignore=W0611
from defcon.status import metrics
# pylama:select=W0611


router = routers.DefaultRouter()
router.register(r'defcon', views.DefConViewSet, 'defcon')
router.register(r'simple', views.SimpleViewSet, 'simple')
router.register(r'components', views.ComponentViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'plugin', views.PluginViewSet)
router.register(r'plugin_instance', views.PluginInstanceViewSet)
router.register(r'status', views.StatusViewSet)

schema_view = get_swagger_view(title='defcon')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^swagger/$', schema_view),
]
