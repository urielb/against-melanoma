
SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = True
SERVE_STATIC = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drderma',
        'USER': 'drderma',
        'PASSWORD': 'drderma',
        'HOST': '',
        'PORT': '',
    }
}

