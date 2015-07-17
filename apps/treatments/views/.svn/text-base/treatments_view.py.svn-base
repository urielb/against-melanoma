# -*- coding: utf-8 -*-
from django.contrib.auth import views as Auth
from datetime import datetime
from datetime import timedelta
import sys
from django.utils.datastructures import MultiValueDictKeyError
from libs.utils import send_error_report

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings

from paypal.standard.ipn.models import PayPalIPN
from django.contrib.auth.models import User
from treatments.models import * # Patient, MARITAL_STATUS_CHOICES
from doctors.models import *
# from accounts.models import Activation
from fileupload.models import Picture
import system
from payment import paypal

from django.views.decorators.csrf import csrf_exempt

# ATTENTION: This should only be available during development phase
'''
def c_p(request, treatment_id):
    
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
        print "Failed to register payment"
        import traceback
        print traceback.format_exc()
        error = traceback.format_exc()
        
        return HttpResponse(error)
    return HttpResponse("Done")
'''

@login_required
def submit_photos(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    user = request.user
    if request.method == "POST":
        post = request.POST
        
        treatment_dict = dict(patient = user.patient)
        
        try:
            pictures_ids = post['pictures_ids']
            pictures_ids = pictures_ids.split(',')
            if len(pictures_ids) < 1:
                error = u"Número minimo de fotos exigidas é 1. Você enviou menos fotos que isso, tente enviar novamente com o número correto de fotos."
                return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))
        except:
            error = u"Ocorreu um erro ao tentar ler as fotos. Tente enviar o formulário novamente mais tarde."
            return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))
            
        for pid in pictures_ids:
            try:
                picture = Picture.objects.get(pk=int(pid))
                treatment_picture = TreatmentPicture.objects.get_or_create(picture=picture, treatment=treatment)
            except:
                import traceback
                error = traceback.format_exc()
                send_error_report("ERROR - Failed to create treatment photos", error)
                for i in treatment.treatment_pictures.all():
                    i.picture.delete()
                treatment.delete()
                error = u"Ocorreu um erro ao tentar processar as novas fotos. Tente novamente mais tarde. Se o erro persistir os administradores serão notificados para resolver o problema o mais rápido possível."
                return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))

            success = u"Novas fotos adicionadas com sucesso! O médico será notificado e prosseguirá com a avaliação em breve."
            treatment.more_photos_submitted()
            return render_to_response("message.html", {'success': success}, context_instance=RequestContext(request))

    if user.is_patient():
        if treatment.patient == user.patient:
            return render_to_response("treatments/submit_photos.html", locals(), context_instance=RequestContext(request))
    error = "You don't have permission to access this treatment."
    return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))
    
@login_required
def get_treatment_results(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    user = request.user
    if user.is_patient() is True:
        if treatment.patient == user.patient:
            treatment_result = treatment.get_latest_status_object()
            doctor = treatment_result.doctor_at_the_time
            return render_to_response("treatments/treatment_results.html", locals(), context_instance=RequestContext(request))
    error = "You don't have permission to access the results of this review."
    return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))
    
# URGENT: FIX THE RESPONSE TEMPLATE
@login_required
def treatment_followup(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    user = request.user
    if user.is_patient() is True:
        if treatment.patient == user.patient:
            treatment_result = treatment.get_latest_status_object()
            doctor = treatment_result.doctor_at_the_time
            return render_to_response("treatments/treatment_results.html", locals(), context_instance=RequestContext(request))
    error = "You don't have permission to access the results of this review."
    return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))

@login_required
def get_payments_info(request, treatment_id):
    entries = PayPalIPN.objects.filter(invoice=treatment_id)
    treatment = Treatment.objects.get(pk=treatment_id)
    return render_to_response("treatments/payments_info.html", locals(), context_instance=RequestContext(request))
'''
@csrf_exempt
def pagseguro_retorno(request):
    post = request.POST
    return render_to_response("pagseguro/retorno.html", locals(), context_instance=RequestContext(request))
'''
    
def payment_complete(request):
    return render_to_response("treatments/payment_complete")
    
@login_required
def check_treatments(request):
    user = request.user
    
    if user.is_doctor() is True:
        post = True
        error = u"Você como médico não tem avaliações em andamento como paciente."
        return render_to_response("message.html", locals(), context_instance=RequestContext(request))
        
    try:
        patient = user.patient
    except:
        raise
    treatments_status = TreatmentStatus.objects.raw('''SELECT * FROM treatments_treatmentstatus ts1 JOIN treatments_treatment t ON t.id = ts1.treatment_id
                                                       WHERE t.patient_id = %s AND ts1.id = (SELECT id FROM treatments_treatmentstatus ts2 
                                                           WHERE ts1.treatment_id = ts2.treatment_id ORDER BY change_date DESC LIMIT 1)
                                                        ORDER BY change_date DESC''' % patient.id)
    # filter(treatment__patient=patient).order_by('-change_date').group_by('treatment')
    treatments = patient.treatments.all().order_by('-datetime')
    return render_to_response("treatments/check_treatments.html", locals(), context_instance=RequestContext(request))

@login_required
def toa_new_treatment(request):
    if request.method == "POST":
        post = request.POST
        accepted = (post.get('accept', False) == "ACEITO")
        if accepted:
            try:
                user = request.user
                treatment = Treatment.objects.filter(patient=user.patient).latest('datetime')
            except:
                raise Http404
            treatment.accepted = accepted
            treatment.save()
            return paypal(request, treatment.id)
            
    return render_to_response("treatments/toa.html", locals(), context_instance=RequestContext(request))

def photo_instructions(request):
    return render_to_response("treatments/photo_instructions.html", context_instance=RequestContext(request))

@login_required
def start_new_treatment(request):
    appearance_time_scale_choices = Treatment.time_scale_choices
    
    num_photos = system.GET_MIN_NUM_PHOTOS()
    
    user = request.user
    
    if user.is_doctor() is True:
        post = True
        error = u"Você como médico não pode iniciar uma avaliação."
        return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))
    
    if request.method == "POST":
        post = request.POST
        
        treatment_dict = dict(patient = user.patient)
        
        try:
            pictures_ids = post['pictures_ids']
            pictures_ids = pictures_ids.split(',')
            if len(pictures_ids) < num_photos:
                error = u"Número mínimo de fotos exigidas são %s. Você enviou menos fotos que isso, tente enviar novamente com o número correto de fotos." % MIN_NUM_PHOTOS
                return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))
        except:
            error = u"Ocorreu um erro ao tentar ler as fotos. Tente enviar o formulário novamente mais tarde."
            return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))
        
        try:
            treatment_dict.update(dict(
            multiple_lesions = (post['multiple_lesions'] == "multiple"),
            appearance_time_scale = post['appearance_time_scale'],
            appearance_time = int(post['appearance_time']),
            permanent = (post['permanent'] == "true"),
            currently_undergoing_treatment = (post['currently_undergoing_treatment'] == "true"),
            family_history = (post['family_history'] == "true")
            ))
        except:
            error = u"Erro ao processar campos do formulario. Tente novamente, preenchendo todos os campos corretamente."
            return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))
        
        try:
            treatment_dict.update(dict(
            itches = (post.get('itches', False) == "true"),
            burns = (post.get('burns', False) == "true"),
            hurts = (post.get('hurts', False) == "true"),
            continuously_itchy = (post.get('continuously_itchy', False) == "true"),
            itchy_during_daytime = (post.get('itchy_during_daytime', False) == "true"),
            itchy_during_nighttime = (post.get('itchy_during_nighttime', False) == "true"),
            numb = (post.get('numb', False) == "true"),
            sensitive_to_touch = (post.get('sensitive_to_touch', False) == "true"),
            has_grown = (post.get('has_grown', False) == "true"),
            has_changed_spread = (post.get('has_changed_spread', False) == "true")
            ))
        except MultiValueDictKeyError:
            pass
            
        treatment_dict.update(dict(
        currently_undergoing_treatment_obs = post['currently_undergoing_treatment_obs'],
        family_history_obs = post['family_history_obs']
        ))
        
        treatment = Treatment(**treatment_dict)
        
        treatment.save()
        
        for pid in pictures_ids:
            try:
                picture = Picture.objects.get(pk=int(pid))
                treatment_picture = TreatmentPicture.objects.get_or_create(picture=picture, treatment=treatment)
            except:
                import traceback
                error = traceback.format_exc()
                send_error_report("ERROR - Failed to create treatment photos", error)
                for i in treatment.treatment_pictures.all():
                    i.picture.delete()
                treatment.delete()
                error = u"Ocorreu um erro duranto o processamento dos dados."
                return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))

        success = "Consulta registrada com sucesso!"
        
        request.method = "GET"
        return toa_new_treatment(request)
        
    return render_to_response("treatments/start_new_treatment.html", locals(), context_instance=RequestContext(request))
