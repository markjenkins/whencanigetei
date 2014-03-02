from django.conf.urls import patterns, url

from whenei.views import handle_request

urlpatterns = patterns(
    '',
    url(r'^.*$', handle_request),
)
