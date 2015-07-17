from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
import datetime

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def upload_to(instance, filename):
    patient = instance.user.patient
    pgid = (patient.id / 10000) + 1
    f = "treatments/photos/%09d/%s" % (pgid, patient.id)
    ensure_dir(settings.MEDIA_ROOT + "/" + f)
    return "%s/%s" % (f, filename)
    
def thumb_upload_to(instance, filename):
    patient = instance.user.patient
    pgid = (patient.id / 10000) + 1
    f = "treatments/photos/%09d/%s/thumbs/" % (pgid, patient.id)
    ensure_dir(settings.MEDIA_ROOT + "/" + f)
    return "%s/%s" % (f, filename)

def upload_url(patient):
    pgid = (patient.id / 10000) + 1
    f = "treatments/photos/%09d/%s" % (pgid, patient.id)
    return "%s" % f
    
def thumb_upload_url(patient):
    pgid = (patient.id / 10000) + 1
    f = "treatments/photos/%09d/%s/thumbs" % (pgid, patient.id)
    return "%s" % f

class Picture(models.Model):

    # This is a small demo using just two fields. The slug field is really not
    # necessary, but makes the code simpler. ImageField depends on PIL or
    # pillow (where Pillow is easily installable in a virtualenv. If you have
    # problems installing pillow, use a more generic FileField instead.

    #file = models.FileField(upload_to="pictures")
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    file = models.ImageField(upload_to=upload_to, max_length=200)
    thumb = models.ImageField(upload_to=thumb_upload_to, max_length=200)
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.slug

    #@models.permalink
    def get_absolute_url(self):
        return "%s%s/%s" % (settings.MEDIA_URL, upload_url(self.user.patient), self.slug)
        
    def get_thumb_url(self):
        return "%s%s/%s" % (settings.MEDIA_URL, thumb_upload_url(self.user.patient), self.slug)

    def save(self, *args, **kwargs):
        self.slug = self.file.name.split("/")[-1:][0]
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
