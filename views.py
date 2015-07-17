# -*- coding: utf-8 -*-

from django.contrib.auth import views as Auth
from datetime import datetime
from datetime import timedelta

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from mailer import send_mail
from django.db.models import Q

from django.utils.translation import ugettext_lazy as _

def test_checkout(request):
    from treatments.models import Treatment
    from treatments.views import paypal
    
    treatment_id = request.GET['id']
    
    return paypal(request, treatment_id)

# @login_required
def index(request):
    # return HttpResponse("HEKLO")
    user = request.user
    logged = user.is_authenticated()
    
    if logged:
        if user.is_patient():
            alerts = user.patient.get_alerts()
            template = "patients/index.html"
        elif user.is_doctor():
            treatments = user.doctor.get_open_treatments()
            from treatments.models import TreatmentQueue, TreatmentStatus
            this_month = len(TreatmentStatus.objects.filter(doctor_at_the_time=user.doctor, status="EC", change_date__gte=(datetime.now() - timedelta(days=30)) ))
            monthly_total = TreatmentStatus.objects.raw('''SELECT id FROM treatments_treatmentstatus ts1
                                                               WHERE id = (SELECT id FROM treatments_treatmentstatus ts2
                                                                   WHERE ts1.treatment_id = ts2.treatment_id ORDER BY change_date DESC LIMIT 1)
                                                                ORDER BY change_date DESC''')
            monthly_total = len(list(monthly_total))
            queue_length = TreatmentQueue.get_queue_length()
            template = "doctors/index.html"
        else:
            template = "staff/index.html"
    else:
        template = "base_with_hero_unit.html"
    
    try:
        next = next
    except:
        next = reverse('index')
        
    return render_to_response(template, locals(), context_instance=RequestContext(request)) # "home.html", locals()) #, context_instance=RequestContext(request))
    
def about_us(request):
    return render_to_response("about_us.html", {}, context_instance=RequestContext(request))
    
def terms(request):
    return render_to_response("terms.html", {}, context_instance=RequestContext(request))
    
def faq(request):
    return render_to_response("faq.html", {}, context_instance=RequestContext(request))
    
def submit_contact_form(request):
    if request.method == "POST":
        post = request.POST
        user = request.user
        name = ""
        email = ""
        subject_f = post['subject']
        message = post['message']
        if user.is_authenticated():
            name = user.get_full_name()
            email = user.email
        else:
            name = post['name']
            email = post['email']
        
        subject = "Dr.Derma - Contato de usuario (%s - %s)" % (name, subject_f)
        body = """Dr.Derma - Contato de usuario (%s)\n
                  Usuario: %s\n
                  Email: %s\n
                  Assunto: %s\n
                  Mensagem: %s""" % (subject_f, name, email, subject_f, message)
        sender = "%s" % email
        to = [settings.CONTACT_CENTER]
        send_mail(subject, body, sender, to)
        
        success = _(u"Seu contato foi feito com sucesso. Tentaremos retornar o contato o mais breve possivel. Obrigado!")
        return render_to_response("message.html", {"success": success}, context_instance=RequestContext(request))
    else:
        error = _(u"Método de acesso inválido.")
    
    return render_to_response("message.html", {"error": error}, context_instance=RequestContext(request))
    
def contact(request):
    return render_to_response("contact.html", {}, context_instance=RequestContext(request))