from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from treatments.models import TreatmentQueue, Treatment
from django.utils.translation import ugettext_lazy as _
# from treatments.models import TreatmentDoctor

from django.db.models import Q

import datetime
        
def is_doctor(self):
    try:
        doctor = Doctor.objects.filter(user=self)
        if len(doctor) > 0:
            return True
        else:
            return False
    except:
        return False

User.add_to_class('is_doctor', is_doctor)

class Doctor(models.Model):
    user = models.OneToOneField(User)
    crm = models.CharField(_('crm'), blank=True, max_length=100)
    
    def __unicode__(self):
        return u"Dr. %s" % self.user.get_full_name()
        
    # TODO: IMPORTANT: This method must implement the rules to check if the doctor is allowed to get another treatment at the momment
    def can_get_new_treatment(self):
        return True
    
    def get_new_treatment(self):
        treatment_item = TreatmentQueue.get_treatment()
        if treatment_item is not None:
            treatment_item.forward()
            treatment = treatment_item.treatment
            treatment.forward_to(self)
            treatment.set_status("WDR")
            treatment.save()
            return True
        else:
            return False
    
    def get_open_treatments(self):
        treatments_doctor = self.treatments.all()
        treatments = []
        for i in treatments_doctor:
            if i.treatment.get_latest_status_object().status != "EC":
                treatments.append(i)
        return treatments
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    class Meta:
        app_label = "doctors"

"""
class DoctorQueue(models.Model):
    ""(DoctorQueue description)""
    doctor = models.ForeignKey(Doctor, related_name='doctor')
    entry_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    desired_amount = models.IntegerField(blank=True, null=True)

#    class Admin:
#        list_display = ('doctor','entry_date','desired_amount',)
#        search_fields = ('doctor',)

    def __unicode__(self):
        return u"DoctorQueue"

    class Meta:
        app_label = "doctors"
        ordering = ['-entry_date']
        
    @staticmethod
    def assign_treatment():
        return True

    @staticmethod
    def is_empty():
        if DoctorQueue.objects.all() == []:
            return True
        return False
"""
# admin.site.register(DoctorQueue)
