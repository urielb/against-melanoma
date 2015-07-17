SITE_ID = 1

SITE_URL = "http://example.drderma.bertoche.com.br"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drderma',
        'USER': 'drderma',
        'PASSWORD': 'K32tHeUNAUFUShNX',
        'HOST': '',
        'PORT': '',
    }
}
