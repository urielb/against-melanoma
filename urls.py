from django.conf.urls.defaults import patterns, include, url
# from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from settings import is_production

# from autocomplete.views import autocomplete

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_project.views.home', name='home'),
    # url(r'^my_project/', include('my_project.foo.urls')),
    # TODO: Remove after testing
    url(r'^co/$', 'views.test_checkout', name='test_checkout'),
    ## end remove
    url(r'^$', 'views.index', name='index'),
    url(r'^about-us/$', 'views.about_us', name='about_us'),
    url(r'^faq/$', 'views.faq', name='faq'),
    url(r'^contact/$', 'views.contact', name='contact'),
    url(r'^terms/$', 'views.terms', name='terms'),
    url(r'^submit_contact_form/$', 'views.submit_contact_form', name='submit_contact_form'),
    
    url(r'^accounts/login', 'django.contrib.auth.views.login', name='my_login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', name='my_logout'),
    url(r'^accounts/(?P<action>(activate|cancel))/(?P<confirmation_key>\w{40})/$', 'accounts.views.activate', name='activate_account'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^patients/', include('patients.urls')),
    url(r'^doctors/', include('doctors.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^treatments/', include('treatments.urls')),
    url(r'^fileupload/', include('fileupload.urls')),
    url(r'^treatments/checkout/(?P<treatment_id>\w{16})/$', 'treatments.views.paypal', name='paypal'),
    # url(r'^treatments/checkout_pro/(?P<treatment_id>\w{16})/$', 'treatments.views.paypal_pro', name='paypal_pro'),
    url(r'^treatments/paypalreturn/$', 'treatments.views.paypalreturn', name='paypalreturn'),
    url(r'^treatments/paypal-cancel-return/$', 'treatments.views.paypal_cancel_return', name='paypal-cancel-return'),
)

# Password reset url's
urlpatterns += patterns('',
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
    # ...
)


if not is_production():
    urlpatterns += patterns('django.contrib.staticfiles.views',
            url(r'^static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
        ) 
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )

urlpatterns += patterns('',
        (r'^C8YCR93/U/F/6D06CH4M/', include('paypal.standard.ipn.urls')),
    )
