from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

class Notification(models.Model):
    """Module to create notifications for users. Using signals to create new notifications passing message and user as parameters."""
    user = models.ForeignKey(User, related_name='notifications')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    message = models.CharField(_('Mensagem'), blank=True, max_length=512)
    hidden = models.BooleanField(default=False)
    style = models.CharField(_('style'), blank=True, max_length=100)
    
    def hide(self):
        self.hidden = True
        try:
            self.save()
        except:
            return False
        return True

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"%s (%s)" % (message, datetime)

    class Meta:
        app_label = "notifications"
        ordering = ['-datetime']