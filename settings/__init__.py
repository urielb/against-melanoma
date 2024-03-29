# -*- coding: utf-8 -*-
"""
    nome
    ~~~~~~~~~~~~~~

    Here goes the description of this file.

    :copyright: (c) 2012 by urielbertoche.
"""

MAIN_DOCTOR_EMAIL = "uriel.bertoche@uniriotec.br"

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)
if not SITE_ROOT in sys.path:
    sys.path.append(SITE_ROOT)

if not os.path.join(PROJECT_ROOT,'apps') in sys.path:
    sys.path.append(os.path.join(PROJECT_ROOT, PROJECT_ROOT,'apps'))
if not os.path.join(PROJECT_ROOT,PROJECT_ROOT, 'libs') in sys.path:
    sys.path.append(os.path.join(PROJECT_ROOT,PROJECT_ROOT, 'libs'))

SECRET_KEY = 'asdasuda9sd7a9sda6sd5asdr7asa8jns4dasdhas'

IN_PRODUCTION = os.environ.get('IN_PRODUCTION', False)
CURRENT_ENV = os.environ.get('CURRENT_ENV', 'DEV')

LOGIN_URL = '/accounts/login' #'/drderma/accounts/login'

from django.core.urlresolvers import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('index')

from config import *
from installed_apps import *
from logging import *
from paypal import *
from emails import *

if CURRENT_ENV == "DEV":
    NO_DEPRECATION_WARNINGS=True
    from env_prod import *
else:
    NO_DEPRECATION_WARNINGS=False
    from env_prod import *

if NO_DEPRECATION_WARNINGS:
    import warnings
    warnings.simplefilter('ignore', DeprecationWarning)


