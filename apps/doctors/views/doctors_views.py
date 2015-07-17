# -*- coding: utf-8 -*-
from django.contrib.auth import views as Auth
from datetime import datetime
from datetime import timedelta
import sys
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import MultiValueDictKeyError

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import available_attrs
from django.template import RequestContext
from django.conf import settings

from paypal.standard.ipn.models import PayPalIPN
from django.contrib.auth.models import User
from treatments.models import * # Patient, MARITAL_STATUS_CHOICES
from doctors.models import *
# from accounts.models import Activation
from fileupload.models import Picture
from views import index
from libs.json_response import json_200, json_500

# from doctors.decorators import *
def pass_or_error(test_func, error=""):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_doctor():
                return view_func(request, *args, **kwargs)
            else:
                return render_to_response("message.html", {'error': error}, context_instance=RequestContext(request))
        return _wrapped_view
    return decorator
    
def user_is_doctor(function=None):
    actual_decorator = pass_or_error(
        lambda u: u.is_doctor(),
        error = u"Você precisa ser um médico para acessar essa área."
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_treatment_doctor(user, treatment_id):
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except:
        return False
    doctor = user.doctor
    return treatment.get_current_doctor() == doctor
    
@login_required
@user_is_doctor
def make_review(request):
    user = request.user
    if request.method != "POST":
        return json_500(500, u"Método de acesso inválido.")
    
    post = request.POST
    treatment_id = post['treatment_id']
    review = post['review']
    if treatment_id == "":
        return json_500(500, u"Dados inválidos.")
    
    if is_treatment_doctor(user, treatment_id) is not True:
        return json_500(500, u"Não autorizado.")
        
    treatment = Treatment.objects.get(id=treatment_id)
    status, success = treatment.set_status("EC")
    status.obs = review
    status.save()
    
    return json_200(u"Avaliação enviada com sucesso.")
    
@login_required
@user_is_doctor
def treatments_history(request):
    user = request.user
    treatments = user.doctor.treatments.all()
    return render_to_response("doctors/treatments_history.html", locals(), context_instance=RequestContext(request))
    

@login_required
@user_is_doctor
# re@user_passes_test(is_treatment_doctor)
# @advanced_testing(is_treatment_doctor, "request")
def review_treatment(request, treatment_id):
    user = request.user
    if is_treatment_doctor(user, treatment_id) is True:
        treatment = Treatment.objects.get(id=treatment_id)
        now = datetime.datetime.now()
        treatment_pictures = treatment.treatment_pictures.all()
        return render_to_response("doctors/review_treatment.html", locals(), context_instance=RequestContext(request))
    return HttpResponse(u"SEM PERMISSÃO")
    
@login_required
@user_is_doctor
def request_more_photos(request):
    if request.method != "POST":
        hr = HttpResponse(u"Método de acesso inválido.")
        hr.status_code = 500
        return hr
        
    post = request.POST
    doctor = request.user.doctor
    treatment_id = post['treatment_id']
    obs = post['obs']
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except:
        hr = HttpResponse(u"Avaliação não encontrada.")
        hr.status_code = 500
        return hr
    
    if treatment.get_current_doctor() != doctor:
        hr = HttpResponse(u"Você não tem permissão para interagir com essa avaliação!")
        hr.status_code = 500
        return hr
        
    treatment.request_more_photos(obs)
    
    return HttpResponse(u"Avaliação atualizada com sucesso.")
    
    
@login_required
@user_is_doctor
def get_new_treatment(request):
    # TODO: URGENT!! WORK ON PROCCESS
    user = request.user
    doctor = user.doctor
    
    if doctor.can_get_new_treatment():
        result = doctor.get_new_treatment()
        if result is False:
            result = json_500(501, u"%s" % _(u"Não existem avaliações na fila de espera.").__unicode__())
        else:
            result = json_200(u"%s" % _(u"Avaliação requerida com sucesso.").__unicode__())
    else:
        result = json_500(500, u"%s" % _(u"Você não pode requerer uma nova avaliação no momento.").__unicode__())
    
    return result