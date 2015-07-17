# -*- coding: utf-8 -*-

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from treatments.models import Treatment, TreatmentStatus, TreatmentQueue
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from paypal.pro.views import PayPalPro
import system
from system.models import Config
from libs.utils import send_error_report

@csrf_exempt
def paypalreturn(request):
    return render_to_response("paypal/return.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def paypal_cancel_return(request):
    return render_to_response("paypal/cancel-return.html", locals(), context_instance=RequestContext(request))
    
def message_error(message):
    return render_to_response("message.html", {"error": message}, context_instance=RequestContext(request))
    
def free_treatment(request):
    if request.method == "POST":
        post = request.POST
        try:
            treatment_id = post['treatment_id']
        except:
            return message_error(u"Formulário inválido.")
        
        try:
            treatment = Treatment.objects.get(id=treatment_id)
        except:
            return message_error(u"Avaliação não encontrada.")
            
        if system.GET_FREE_TREATMENTS() > 0:
            f_t = Config.objects.get(key="free_treatments")
            f_t.value = int(f_t.value) - 1
            f_t.save()
        else:
            return message_error(u"Não existem mais gratuidades no momento.")
            
        try:
            treatment.paid = True
            treatment.save()

            treatment_status = TreatmentStatus(status="IQ", treatment=treatment)
            treatment_status.save()

            treatment_queue = TreatmentQueue(treatment=treatment)
            treatment_queue.save()
        except:
            import traceback
            error = traceback.format_exc()
            subject = "ERROR - Failed to completed payment procedure"
            send_error_report(subject, error)
            
        return render_to_response("message.html", {"success": u"Avaliação enviada com sucesso. Já se encontra na fila de espera. Você será notificado das atualizações na sua avaliação pelo sistema e pelo seu email registrado. Aguarde."}, context_instance=RequestContext(request))
    else:
        return message_error(u"Não pode ser acessado dessa maneira.")

def paypal(request, treatment_id):

    # What you want the button to do.
    
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except:
        raise Http404
        
    treatment_price = system.GET_TREATMENT_PRICE()
    treatment_time = system.GET_TREATMENT_TIME_LIMIT()
        
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "charset": "utf-8",
        "amount": "%s" % treatment_price,
        "item_name": u"Avaliação e Orientação Dermatológica",
        "custom": treatment_id,
        "invoice": treatment_id,
        "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
        "return_url": "%s%s" % (settings.SITE_NAME, reverse('paypalreturn')),
        "cancel_return": "%s%s" % (settings.SITE_NAME, reverse('paypal-cancel-return')),
    }

    # Create the instance.
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    
    free_treatments = system.GET_FREE_TREATMENTS()
    
    if settings.PAYPAL_TEST:
        paypal_form = paypal_form.sandbox()
    else:
        paypal_form = paypal_form.render()
    context = {"paypal_form": paypal_form, "treatment": treatment, "treatment_time": treatment_time, "free_treatments": free_treatments}
    return render_to_response("treatments/checkout.html", context, context_instance=RequestContext(request))
    
    from paypal.pro.views import PayPalPro

def paypal_pro(request, treatment_id):
    
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except:
        raise Http404
    
    item = {"amt": "0.10",             # amount to charge for item
            "currencycode": "BRL",
            "inv": treatment.id,         # unique tracking variable paypal
            "custom": treatment.id,       # custom tracking variable for you
            "cancelurl": "http://...",  # Express checkout cancel url
            "returnurl": "%s%s" % (settings.SITE_NAME, reverse('paypalreturn')), }  # Express checkout return url

    items = []
    items.append(treatment)

    kw = {"item": item,                            # what you're selling
          "payment_template": "paypal/payment.html",      # template name for payment
          "confirm_template": "paypal/confirmation.html", # template name for confirmation
          "success_url": "%s%s" % (settings.SITE_NAME, reverse('paypalreturn'))}              # redirect location after success

    ppp = PayPalPro(**kw)
    return ppp(request)
