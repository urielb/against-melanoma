# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

"""
class Location(models.Model):
    country = models.CharField(_('Pais'), blank=True, max_length=100)
    state   = models.CharField(_('Estado'), blank=True, max_length=100)
    city    = models.CharField(_('Cidade'), blank=True, max_length=100)
    
    class Admin:
        list_display = ('', )
        search_fields = ('country', 'state', )
        
    class Meta:
        app_label = "patients"
    
    def __unicode__(self):
        return u"%s - %s, %s" % (self.city, self.state, self.country)
"""
    
"""
class PhoneNumber(models.Model):
    patient      = models.ForeignKey('Patient')
    country_code = models.CharField(_('Codigo do Pais'), default='+55', max_length=4)
    area_code    = models.CharField(_('Codigo de Area'), blank=True, max_length=4)
    number       = models.CharField(_('Numero'), max_length=15)

    class Admin:
        list_display = ('',)
        search_fields = ('country_code','area_code', )
    
    class Meta:
        app_label = "patients"
    def __unicode__(self):
        return u"%s (%s) %s-%s" % (self.country_code, self.area_code, self.number[:len(self.number)/2], self.number[len(self.number)/2:])
"""

def is_patient(self):
    try:
        patient = Patient.objects.filter(user=self)
        if len(patient) > 0:
            return True
        else:
            return False
    except:
        return False

User.add_to_class('is_patient', is_patient)

class Patient(models.Model):
    SEX_CHOICES = (
        ('M', _('Masculino')),
        ('F', _('Feminino')),
    )

    """
    MARITAL_STATUS_CHOICES = (
        ('SI', _('Solteiro')),
        ('MA', _('Casado')),
        ('DI', _('Divorciado')),
        ('WI', _('Vivuo')),
        ('CO', _('Cohabitando')),
        ('CU', _('Uniao Civil')),
        ('DP', _('Parceria domestica')),
        ('UP', _('Parceiros nao casados')),
    )
    """
    
    user             = models.OneToOneField(User, related_name=_('patient'))
    sex              = models.CharField(_('Sexo'), max_length=1, choices=SEX_CHOICES)
    date_of_birth    = models.DateField(_('Data de nascimento'))
    # marital_status   = models.CharField(_('Estado civil'), max_length=2, choices=MARITAL_STATUS_CHOICES)
    # occupation       = models.CharField(_('Ocupacap'), blank=True, max_length=100)
    # birth_location   = models.ForeignKey(Location, related_name='birth_location') # maybe change field name to "birth_place"
    # current_address  = models.ForeignKey(Location, related_name='current_address')
    
    def get_sex(self):
        return dict(Patient.SEX_CHOICES)[self.sex]
    
    def get_alerts(self):
        last_login = self.user.last_login
        treatments = self.treatments.filter(treatment_status__change_date__gte=last_login).distinct() # order_by('-treatment_status__change_date').distinct("id")
        status = []
        for i in treatments:
            for j in i.treatment_status.filter(change_date__gte=last_login).order_by('-change_date'):
                status.append(j)
        
        alerts = []
        for i in status:
            alerts.append({'type': _(u'Avaliação'), 'id': i.treatment.id, 'message': i.get_status(), 'date': i.change_date, 'priority': 'info'})
            
        return alerts

    class Meta:
        app_label = "patients"

    class Admin:
        list_display = ('', )
        search_fields = ('user.first_name', 'user.last_name', 'user.email', 'telefone_numbers')
        
    def __unicode__(self):
        return u"%s" % self.user.get_full_name()