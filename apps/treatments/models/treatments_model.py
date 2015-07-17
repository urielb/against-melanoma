# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from patients.models import Patient
from fileupload.models import Picture
import datetime
from mailer import send_mail
from libs.utils import random_string
from system.models import Config
import system

class TreatmentQueue(models.Model):
    priority = models.IntegerField(default=0, blank=True, null=True)
    treatment = models.ForeignKey('Treatment', related_name='treatment_queue')
    entry_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    forwarded = models.BooleanField(default=False)
    
    @staticmethod
    def get_unforwarded_treatments():
        return TreatmentQueue.objects.filter(forwarded=False).order_by('entry_date').order_by('-priority')
        
    @staticmethod
    def get_queue_length():
        return len(TreatmentQueue.get_unforwarded_treatments())
        
    @staticmethod
    def is_empty():
        if len(TreatmentQueue.get_unforwarded_treatments()) == 0:
            return True
        return False
        
    @staticmethod
    def get_treatment():
        if TreatmentQueue.is_empty():
            return None
            
        treatment = TreatmentQueue.get_unforwarded_treatments()[0]
        
        return treatment
        
    def forward(self):
        self.forwarded = True
        self.save()
        return True
        
    def __unicode__(self):
        return u"%s (%s)" % (self.treatment.id, self.forwarded)
        
    def save(self, *args, **kwargs):
        in_queue = TreatmentQueue.objects.filter(treatment=self.treatment)
        if len(in_queue) > 0:
            if self.id == in_queue[0].id and self.id is not None:
                super(TreatmentQueue, self).save(*args, **kwargs)
        else:
            super(TreatmentQueue, self).save(*args, **kwargs)
    
    class Meta:
        app_label = "treatments"

class TreatmentStatus(models.Model):
    treatment_status = (
        ("APC", _(u"Aguardando confirmação de pagamento")), # APC = Awaiting payment confirmation
        ("IQ", _("Em fila de espera")), # IQ = In Queue
        ("WDR", _(u"Aguardando avaliação")), # WDR = Waiting Doctor Review
        ("EIP", _(u"Em avaliação médica")), # EIP = Evaluation in Progress
        ("EC", _(u"Concluído pelo médico")), # EC = Evaluation Concluded
        ("NOP", _(u"Requer fotos adicionais")), # NOP = Need Other Pictures
        ("CDP", _(u"Sendo encaminhada para um médico")), # CDP = Changing Doctors Proccess
    )
    
    treatment = models.ForeignKey('Treatment', related_name='treatment_status')
    change_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    doctor_at_the_time = models.ForeignKey("doctors.Doctor", blank=True, null=True, related_name='doctor_at_the_time')
    status = models.CharField(_('Status'), blank=True, max_length=5, choices=treatment_status)
    obs = models.TextField(blank=True)
    
    def get_status(self):
        return dict(TreatmentStatus.treatment_status)[self.status]
    
    class Meta:
        app_label = "treatments"

class Treatment(models.Model):
    """(Treatment description)"""
    time_scale_choices = (
        ("Days", _("Dias")),
        ("Months", _("Meses")),
        ("Years", _("Anos"))
    )
    id = models.CharField(_('id'), blank=True, max_length=16, primary_key=True)
    patient = models.ForeignKey(Patient, related_name='treatments')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    paid = models.BooleanField(default=False) # set to True after Paypal completion confirmation
    accepted = models.BooleanField(default=False)
    
    multiple_lesions = models.BooleanField(default=False)
    appearance_time_scale = models.CharField(_('Escala de tempo'), blank=True, max_length=10, choices=time_scale_choices)
    appearance_time = models.IntegerField(blank=True, null=True)
    permanent = models.BooleanField(default=True)
    itches = models.BooleanField(default=False)
    burns = models.BooleanField(default=False)
    hurts = models.BooleanField(default=False)
    continuously_itchy = models.BooleanField(default=False)
    itchy_during_daytime = models.BooleanField(default=False)
    itchy_during_nighttime = models.BooleanField(default=False)
    numb = models.BooleanField(default=False)
    sensitive_to_touch = models.BooleanField(default=False)
    has_grown = models.BooleanField(default=False)
    has_changed_spread = models.BooleanField(default=False)
    currently_undergoing_treatment = models.BooleanField(default=False)
    currently_undergoing_treatment_obs = models.CharField(_('Observações do tratamento atual'), blank=True, max_length=255)
    family_history = models.BooleanField(default=False)
    family_history_obs = models.CharField(_('Observações de histórico familiar'), blank=True, max_length=255)
    
    def price(self):
        return system.GET_TREATMENT_PRICE()
    
    def get_appearance_time_scale(self):
        return dict(Treatment.time_scale_choices)[self.appearance_time_scale]
    
    def get_current_doctor(self):
        try:
            doctor = self.doctors.latest('datetime').doctor
        except:
            return None
        return doctor
    
    def set_status(self, status):
        doctor = self.get_current_doctor()
        treatment = TreatmentStatus.objects.create(treatment=self, doctor_at_the_time=doctor, status=status)
        return treatment, True
    
    def more_photos_submitted(self):
        try:
            TreatmentStatus.objects.create(treatment=self, doctor_at_the_time=self.doctors.latest('datetime').doctor, status="WDR", obs="More photos submitted by the patient")
        except:
            raise
        return True
    
    def request_more_photos(self, obs):
        try:
            TreatmentStatus.objects.create(treatment=self, doctor_at_the_time=self.doctors.latest('datetime').doctor, status="NOP", obs=obs)
        except:
            raise
        return True
    
    def forward_to(self, doctor):
        try:
            if len(self.doctors.all()) > 0:
                TreatmentStatus.objects.create(treatment=self, doctor_at_the_time=self.doctors.latest('datetime').doctor, status="CDP")
                DoctorTreatment.objects.get_or_create(treatment=self, doctor=doctor)
            else:
                TreatmentStatus.objects.create(treatment=self, status="CDP")
                DoctorTreatment.objects.get_or_create(treatment=self, doctor=doctor)
        except:
            raise
        return True
        
    def get_latest_status_object(self):
        try:
            return self.treatment_status.all().order_by("-id")[0]
            # return self.treatment_status.latest("change_date")
        except:
            return False
    
    def on_queue(self):
        in_queue = TreatmentQueue.objects.filter(treatment=self, forwarded=False)
        if len(in_queue) == 0:
            return False
        return True
    
    def save(self, *args, **kwargs):
        import string
        if self.id is None or self.id == '':
            while True:
                self.id = random_string(16, string.digits+string.uppercase)
                try:
                    Treatment.objects.get(pk=self.id)
                except:
                    break
        
        super(Treatment, self).save(*args, **kwargs)
        try:
            if self.get_latest_status_object() == False:
                treatment_status = TreatmentStatus(status="APC", treatment=self)
                treatment_status.save()
        except:
            raise
        # in_queue = TreatmentQueue.objects.filter(treatment=self)
        # if len(in_queue) == 0:
        #     TreatmentQueue.objects.create(treatment=self)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"Treatment for: %s (%s)" % (self.patient, self.datetime)
        
    def get_latest_status(self):
        status = ""
        try:
            status = self.treatment_status.all().order_by("-id")[0]
            status = dict(TreatmentStatus.treatment_status)[status.status]
        except:
            status = "Failed to get treatment status. Please contact the support team."
        return status
        
    def is_closed(self):
        return self.get_latest_status_object().status == "EC"
            
    def is_waiting_photos(self):
        return self.get_latest_status_object().status == "NOP"
        
    def textized(self):
        text = ""
        if self.multiple_lesions:
            text += u"%s" % _(u"As lesões são múltiplas")
        else:
            text += u"%s" % _(u"A lesão é única")
        text += u"\n"
        text += u"%s: %s %s\n" % (_("Apareceu a "), self.appearance_time, dict(Treatment.time_scale_choices)[self.appearance_time_scale])
        if self.permanent:
            text += u"%s" % _(u"A lesão é permanente")
        else:
            text += u"%s" % _(u"A lesão aparece e desaparece")
        text += u"\n"
        if self.itches:
            text += u"%s" % _(u"Coça")
            if self.continuously_itchy:
                text += u"%s" % _(" - O tempo todo")
            if self.itchy_during_daytime:
                text += u"%s" % _(" - Durante o dia")
            if self.itchy_during_nighttime:
                text += u"%s" % _(" - Durante a noite")
            text += u"\n"
        if self.burns:
            text += u"%s\n" % _("Queima")
        if self.hurts:
            text += u"%s\n" % _("Doi")
        if self.numb:
            text += u"%s\n" % _(u"Há dormência no local")
        if self.sensitive_to_touch:
            text += u"%s\n" % _(u"É sensível ao toque")
        else:
            text += u"%s\n" % _(u"Não há sensibilidade no local")
        if self.has_grown:
            text += u"%s\n" % _(u"Aumentou em número desde o aparecimento")
        if self.has_changed_spread:
            text += u"%s\n" % _("Mudou ou espalhou pelo corpo")
        if self.currently_undergoing_treatment:
            text += u"%s\n\t%s:\n\t%s\n" % (_(u"Atualmente o paciente está fazendo um tratamento para a lesão"), _(u"Observações:"), self.currently_undergoing_treatment_obs)
        if self.family_history:
            text += u"%s\n\t%s:\n\t%s\n" % (_(u"A família do paciente tem histórico de cancer de pele ou outras doenças."), _(u"Observações:"), self.family_history_obs)
        return text
            
    def get_pictures_links(self):
        tp = self.treatment_pictures.all()
        text = ""
        for i in tp:
            text += "%s\n" % i.picture.get_absolute_url()
        return text
        
            
    def send_through_mail(self):
        subject = "Dr.Derma - Nova Consulta - Paciente: %s" % self.patient
        body = u"""Dr.Derma - Nova consulta\n
        Nome do paciente: %s\n
        Data de nascimento: %s\n
        Sexo: %s\n\n
        Informações adicionais sobre o paciente:\n
        %s\n\n
        Links para as fotos:\n
        %s
        """ % (self.patient, self.patient.date_of_birth, self.patient.sex, self.textized(), self.get_pictures_links())
        sender = "%s" % self.patient.user.email
        doctor = self.doctor.all().order_by('-datetime')[:1][0].doctor
        to = [doctor.user.email]
        send_mail(subject, body, sender, to)
        
    class Meta:
        app_label = "treatments"
        
class TreatmentPicture(models.Model): #TODO: Change its name to treatmentPicture
    """(TreatmentPhoto description)"""
    treatment = models.ForeignKey(Treatment, related_name='treatment_pictures')
    # picture = models.ForeignKey(Picture, related_name='picture_treatment')
    picture = models.OneToOneField(Picture)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"TreatmentPhoto"

    class Meta:
        app_label = "treatments"

class DoctorTreatment(models.Model):
    treatment = models.ForeignKey(Treatment, related_name='doctors')
    # treatment = models.OneToOneField(Treatment)
    doctor = models.ForeignKey("doctors.Doctor", related_name='treatments')
    datetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    def time_remaining(self):
        time_limit = datetime.timedelta(hours=Config.treatment_time_limit())
        return (self.datetime + time_limit) - datetime.datetime.now()
        
    def date_limit(self):
        time_limit = datetime.timedelta(hours=Config.treatment_time_limit())
        return self.datetime + time_limit
    
    def __unicode__(self):
        return u"%s - passed to doctor %s at %s" % (self.treatment, self.doctor, self.datetime)
        
    class Meta:
        app_label = "treatments"
