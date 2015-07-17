from django.conf.urls.defaults import *
from fileupload.views import PictureCreateView, PictureDeleteView

urlpatterns = patterns('',
    (r'^new/$', PictureCreateView, {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)

