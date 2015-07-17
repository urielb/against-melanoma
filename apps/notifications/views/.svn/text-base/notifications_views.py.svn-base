from datetime import datetime
import sys
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.conf import settings

from django.contrib.auth.models import User
from notifications.models import *
from libs.json_response import json_200, json_500

@login_required
def hide_notification(request):
    if request.method == "POST":
        user = request.user
        post = request.POST
        
        try:
            notification = Notification.objects.get(pk=int(post['notification_id']))
            notification.hidden = True
            if notification.user != user:
                error = "Voce nao tem permissao para alterar essa notificacao."
                return json_500(500, error)
            notification.save()
        except:
            error = "Falha ao tentar alterar a notificacao."
            return json_500(500, error)
        
        success = "Ocultada."
        return json_200(success)
    else:
        error = "Metodo de acesso invalido"
        return json_500(500, error)