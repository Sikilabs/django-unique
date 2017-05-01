__author__ = 'ibrahim (at) sikilabs (dot) com'
__licence__ = 'MIT'

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^getfile/(?P<unique_url>.+)', 'main.unique.views.get_file',
        name='unique_getfile'),
    url(r'^geturl/(?P<media_id>\d+)', 'main.unique.views.generate_url',
        name='unique_geturl'),
    )
