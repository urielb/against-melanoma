from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('notifications.views',
    url(r'^hide_notification/$', 'hide_notification', name='hide_notification'),
)