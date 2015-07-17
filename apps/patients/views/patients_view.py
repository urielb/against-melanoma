# -*- coding: utf-8 -*-
from django.contrib.auth import views as Auth
from datetime import datetime
from datetime import timedelta

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib.auth.models import User
from patients.models import * # Patient, MARITAL_STATUS_CHOICES
from accounts.models import Activation

def edit_profile(request):
    
    return HttpResponse("Edit")

def register(request):
    if request.method == "POST":
        post = request.POST
        
        try:
            f_name = post['first_name']
            l_name = post['last_name']
            email = post['email']
            password = post['password']
            re_password = post['re_password']
            sex = post['sex']
            d_o_b = post['d_o_b']
        except:
            patient_registered = False
            error = "Erro ao processar campos do formulario. Tente novamente, preenchendo todos os campos corretamente."
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        
        sex = sex.upper()
        
        error_empty = "Campo '%s' em branco. Corrija antes de enviar o formulario novamente."
        if f_name == "":
            error = error_empty % "Nome"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if l_name == "":
            error = error_empty % "Sobrenome"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if email == "":
            error = error_empty % "Email"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if password == "":
            error = error_empty % "Senha"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if password != re_password:
            error = "Senha e confirmacao de senha nao conferem!"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if len(password) < 6:
            errpr = "Senha muito curta, senha precisa ter no minimo 6 caracteres."
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if sex == "":
            error = error_empty % "Sexo"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        if d_o_b == "":
            error = error_empty % "Data de nascimento"
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        
        u = User.objects.filter(email=email)
        
        if len(u) > 0:
            error = "Email ja cadastrado no sistema. Utilize outro email."
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
            
        username = email.replace("@", ".")
        
        try:
            #user = User(username = username, email = email, password = password)
            user = User.objects.create_user(username, email, password)
            user.set_password(password)
        except:
            #import traceback
            #error = traceback.format_exc()
            error = "\nOcorreu um erro ao tentar criar o usuario. Tente novamente mais tarde."
            user.delete()
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
        
        try:
            patient = Patient.objects.create(user=user, sex=sex, date_of_birth=d_o_b)
        except:
            user.delete()
            try:
                patient.delete()
            except:
                pass
            error = "Ocorreu um erro ao cadastrar o usuario. Tente novamente mais tarde."
            return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))
            
            
        user.is_active = False
        user.first_name = f_name
        user.last_name = l_name
        user.save()
            
        activation = Activation.objects.create(user = user, patient = patient)
        activation.send_confirmation_mail()
        success = "Sua conta foi cadastrada com sucesso! Dentro de instantes voce devera receber no seu email cadastrado, um email com o link para ativar sua conta. Se voce nao ativar sua conta nas proximas 72 horas, sua conta sera automaticamente removida. Fique atento!"
        
        patient_registered = True
    return render_to_response("patients/register.html", locals(), context_instance=RequestContext(request))