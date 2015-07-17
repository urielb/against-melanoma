from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('doctors.views',
    url(r'^review_treatment/(?P<treatment_id>\w{16})/$', 'review_treatment', name='review_treatment'),
    url(r'^get_new_treatment/$', 'get_new_treatment', name='get_new_treatment'),
    url(r'^treatments_history/$', 'treatments_history', name='treatments_history'),
    url(r'^request_more_photos/$', 'request_more_photos', name='request_more_photos'),
    url(r'^make_review/$', 'make_review', name='make_review'),
)