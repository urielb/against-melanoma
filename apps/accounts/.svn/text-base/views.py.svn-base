from django.contrib.auth import views as Auth
from datetime import datetime
from datetime import timedelta

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib.auth.models import User
from accounts.models import Activation

def activate(request, action, confirmation_key):
    
    try:
        entry = Activation.objects.get(confirmation_key=confirmation_key)
    except Activation.DoesNotExist:
        entry = None
        
    if entry is None:
        error = "Codigo de confirmacao nao encontrado."
        return render_to_response("accounts/activate.html", locals(), context_instance=RequestContext(request))
    elif not entry.confirmed:
        if action == "activate":
            entry.confirm()
            entry.user.is_active = True
            entry.user.save()
            success = "Sua conta foi ativada com sucesso! Voce esta pronto para logar no sistema."
        elif action == "cancel":
            entry.cancel()
            success = "A conta foi cancelada com sucesso! Voce nao recebera mais emails nossos a nao ser que crie uma conta novamente."
    elif entry.confirmed:
        warning = "Esse codigo ja foi ativado anteriormente."
        return render_to_response("accounts/activate.html", locals(), context_instance=RequestContext(request))
    
    return render_to_response("accounts/activate.html", locals(), context_instance=RequestContext(request))