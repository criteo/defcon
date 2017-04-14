"""defcon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from defcon.status import views


router = routers.DefaultRouter()
router.register(r'components', views.ComponentViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'plugin', views.PluginViewSet)
router.register(r'plugin_instance', views.PluginInstanceViewSet)
router.register(r'status', views.StatusViewSet)

schema_view = get_swagger_view(title='defcon')


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^swagger/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
