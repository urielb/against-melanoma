# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from patients.models import Patient
from fileupload.models import Picture
import datetime
from libs.utils import random_string

class Config(models.Model):
    """(Config description)"""
    key = models.CharField(_('key'), max_length=100)
    description = models.CharField(_('description'), blank=True, max_length=100)
    value = models.CharField(_('value'), max_length=100)

    class Admin(admin.ModelAdmin):
        list_display = ('key','description','value')
        search_fields = ('key',)
        list_editable = ('value',)

    def __unicode__(self):
        return u"Config"

    class Meta:
        app_label = 'system'
        
    @staticmethod
    def free_treatments():
        return int(Config.objects.get(key="free_treatments").value)
        
    @staticmethod
    def treatment_price():
        treatment_price = Config.objects.get(key="treatment_price")
        return float(treatment_price.value)
        
    @staticmethod
    def treatment_time_limit():
        treatment_time_limit = Config.objects.get(key="treatment_time_limit")
        return int(treatment_time_limit.value)
        
    @staticmethod
    def min_num_photos():
        min_num_photos = Config.objects.get(key="min_num_photos")
        return int(min_num_photos.value)

admin.site.register(Config, Config.Admin)