# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from paypal.standard.ipn.signals import payment_was_successful
from paypal.pro.signals import payment_was_successful as payment_was_successful_pro
from treatments_model import Treatment, TreatmentStatus, TreatmentQueue
from django.db.models.signals import pre_save, post_save
from notifications.models import Notification
from mailer import send_mail
from libs.utils import send_error_report
from django.core.urlresolvers import reverse
from settings import SITE_URL

NOP_MAIL_SUBJECT = _(u"Dr. Derma - Mais fotos requistadas para a avaliação #%s")
NOP_MAIL_MESSAGE = u"""O médico responsável pela avaliação requisitou mais fotos para poder completar a orientação, pelos seguintes motivos:
"%s"
Por favor encaminhe mais fotos o mais breve possível para que possamos lhe atender com rapidez.
Link para envio de novas fotos: %s\n
Atenciosamente,
\tEquipe Dr. Derma
"""

EC_MAIL_SUBJECT = _(u"Dr. Derma - Avaliação concluída pelo médico para a avaliação #%s")
EC_MAIL_MESSAGE = u"""O médico responsável pela avaliação concluiu sua orientação.
Para verificar a resposta do médico acesse seu histórico de avaliações pelo link abaixo:
%s

Caso haja algum problema entre em contato com a nossa equipe na área de contato. Obrigado.
Atenciosamente,
\tEquipe Dr. Derma
"""

def send_patients_mail(sender, **kwargs):
    instance = kwargs['instance']
    treatment = instance.treatment
    user = treatment.patient.user
    to = [user.email]
    
    if instance.status == "NOP":
        subject = NOP_MAIL_SUBJECT % treatment.id
        message = NOP_MAIL_MESSAGE % (instance.obs, SITE_URL+reverse('submit_photos', args=(treatment.id,)))
        send_mail(subject, message, "noreply@drderma.com.br", to)
    if instance.status == "EC" and instance.obs != "":
        subject = EC_MAIL_SUBJECT % treatment.id
        message = EC_MAIL_MESSAGE % (SITE_URL+reverse('check_treatments'))
        send_mail(subject, message, "noreply@drderma.com.br", to)
post_save.connect(send_patients_mail, sender=TreatmentStatus)

def create_notification(sender, **kwargs):
    # Your specific logic here
    instance = kwargs['instance']
    treatment = instance.treatment
    user = treatment.patient.user
    if treatment.get_latest_status_object() is not False:
        message = "Saiu de  '%s' para '%s'." % (treatment.get_latest_status_object().get_status_display(), instance.get_status_display())
    else:
        message = "Criada nova avaliacao. Estado inicial: '%s'." % (instance.get_status_display())
    Notification.objects.create(user=user,message=message,style="alert-info")

pre_save.connect(create_notification, sender=TreatmentStatus)

def paypal_payment_completed(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    treatment_id = ipn_obj.invoice
    try:
        treatment = Treatment.objects.get(id = treatment_id)
        treatment.paid = True
        treatment.save()
        
        treatment_status = TreatmentStatus(status="IQ", treatment=treatment)
        treatment_status.save()
        
        treatment_queue = TreatmentQueue(treatment=treatment)
        treatment_queue.save()
    except:
        # TODO: IMPORTANT!
        # Add code to send emails to admins and log the transaction in case of failure
        
        import traceback
        error = traceback.format_exc()
        subject = "ERROR - Failed to completed payment procedure"
        send_error_report(subject, error)
        
    # if ipn_obj.custom == "Upgrade all users!":
    #     print dir(ipn_obj)
    # print dir(ipn_obj)
    # print __file__,1, 'This works'   
         
payment_was_successful.connect(paypal_payment_completed)

"""
def paypal_payment_completed_pro(sender, **kwargs):
    item = sender
    # Undertake some action depending upon `ipn_obj`.
    treatment_id = int(item['custom'])
    
    print item
    
    try:
        treatment = Treatment.objects.get(id = treatment_id)
        treatment.paid = True
        treatment.save()
        
        treatment_status = TreatmentStatus(status="IQ", treatment=treatment)
        treatment_status.save()
    except:
        # TODO: IMPORTANT!
        # Add code to send emails to admins and log the transaction in case of failure
        print "Failed to register payment"

payment_was_successful_pro.connect(paypal_payment_completed_pro)
"""