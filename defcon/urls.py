"""defcon URL Configuration."""

from django.conf.urls import include, url
from django.contrib import admin

from defcon.status import views


urlpatterns = [
    url(r'^status/(?P<component_id>\w+)/', views.status, name='status'),
    url(r'^badge/(?P<component_id>\w+).svg', views.badge, name='badge'),
    url(r'^api/', include('defcon.status.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^health/', include('health_check.urls')),
    url(r'', include('django_prometheus.urls')),
    url(r'', views.index),
]
