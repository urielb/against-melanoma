from fileupload.models import Picture, upload_url, upload_to, thumb_upload_to, thumb_upload_url
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings
from libs.utils import random_string
from libs import pil

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"
        
def PictureCreateView(request):
    if request.POST:
        try:
            f = request.FILES.get('file')
            name = f.name.split('.')
            f.name = "%s.%s" % (random_string(32), name[len(name)-1])
            name = f.name
            p = Picture(user=request.user, file=f)
            p.save()

            image = "%s/%s" % (settings.MEDIA_ROOT, upload_to(p, name))
            thumb = pil.create_thumb(image)
            thumb_address = "%s/%s" % (settings.MEDIA_ROOT, thumb_upload_to(p, name))
            thumb.save(thumb_address)
            thumb_address = "%s%s/%s" % (settings.MEDIA_URL, thumb_upload_url(p.user.patient), name)
            p.thumb = thumb_address
            p.save()
            
            data = [{'id': p.id, 'name': f.name, 'url': settings.MEDIA_URL + upload_url(p.user.patient) + "/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + thumb_upload_url(p.user.patient) + "/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[p.id]), 'delete_type': "DELETE"}]
        except:
            raise
            data = [{'status': 'Error', 'error': 'Error', 'message': 'Failed to submit files'}]
    else:
        data = []
        response = JSONResponse(data, {}, "text/plain")
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    response = JSONResponse(data, {}, "application/json")
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

"""
class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + upload_url(self.request.user.patient) + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + upload_url(self.request.user.patient) + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
"""

class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
