# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from patients.models import Patient
from settings import SITE_URL
from django.utils.hashcompat import sha_constructor
from libs.utils import random_string
from mailer import send_mail
from django.core.urlresolvers import reverse

class Activation(models.Model):
    user = models.ForeignKey(User, related_name='user')
    patient = models.ForeignKey(Patient, related_name='patient')
    confirmation_key = models.CharField(_('Confirmation key'), max_length=40, unique=True)
    confirmed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            salt = random_string(13)
            self.confirmation_key = sha_constructor(salt + self.user.email).hexdigest()
            
            while len(Activation.objects.filter(confirmation_key=self.confirmation_key)) > 0:
                self.confirmation_key = sha_constructor(salt + self.user.email).hexdigest()
            
            self.confirmed = False
        
        super(Activation, self).save(*args, **kwargs)
        
    def confirm(self):
        if not self.confirmed:
            try:
                self.confirmed = True
                self.save()
            except:
                raise Exception("Error while confirming activation code.")
        return True
                
    def cancel(self):
        if not self.confirmed:
            try:
                self.patient.delete()
                self.user.delete()
                self.delete()
            except:
                raise Exception("Error while trying to delete user.")
        return True
                
    def send_confirmation_mail(self):
        subject = u"Dr.Derma - Confirmação de criação de conta"
        body = u"""Dr.Derma - Confirmação de criação de conta\n
                  Recebemos uma requisição para a criação de uma nova conta de usuário no nosso sistema, com esse endereço de email.
                  Para confirmar a criação da nova conta e verificar seu endereço de email, clique no link abaixo ou copie e cole o endereço no seu navegador:\n
                  %s\n\n
                  Caso não tenha sido você quem criou a conta conosco, clique no link abaixo, ou copie e cole no seu navegador:\n
                  %s\n\n
                  Atenciosamente,\n
                  Equipe Dr.Derma.
               """ % (SITE_URL+reverse('activate_account', kwargs={'action': 'activate', 'confirmation_key': self.confirmation_key}), SITE_URL+reverse('activate_account', kwargs={'action': 'cancel', 'confirmation_key': self.confirmation_key}))
        sender = "noreply@drderma.com.br"
        to = [self.user.email]
        send_mail(subject, body, sender, to)