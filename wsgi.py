"""
WSGI config for simpeaq project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

site.addsitedir('/home/urielbertoche/.virtualenvs/drderma/lib/python2.7/site-packages')

sys.path.append('/home/urielbertoche/drderma')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

activate_env=os.path.expanduser("/home/urielbertoche/.virtualenvs/drderma/bin/activate_this.py")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
