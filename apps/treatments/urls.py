from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('treatments.views',
    url(r'^startnew/$', 'start_new_treatment', name='start_new_treatment'),
    url(r'^check_treatments/$', 'check_treatments', name='check_treatments'),
    url(r'^treatment_followup/(?P<treatment_id>\w{16})/$', 'treatment_followup', name='treatment_followup'),
    url(r'^treatment_results/(?P<treatment_id>\w{16})/$', 'get_treatment_results', name='get_treatment_results'),
    url(r'^submit_photos/(?P<treatment_id>\w{16})/$', 'submit_photos', name='submit_photos'),
    url(r'^photo_instructions/$', 'photo_instructions', name='photo_instructions'),
    url(r'^payments_info/(?P<treatment_id>\w{16})/$', 'get_payments_info', name='get_payments_info'),
    url(r'^free_treatment/$', 'free_treatment', name='try_free_treatment'),
    # url(r'^c_p/(?P<treatment_id>\w{16})/$', 'c_p', name='c_p'),
    url(r'^toa/$', 'toa_new_treatment', name='toa_new_treatment'),
    # url(r'^pagseguro/retorno/$', 'pagseguro_retorno', name='pagseguro_retorno')
)