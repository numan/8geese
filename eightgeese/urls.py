from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from okrs.api.resources import ObjectivesResource, KeyResultsResource

v1_api = Api(api_name='v1')
v1_api.register(ObjectivesResource())
v1_api.register(KeyResultsResource())

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
