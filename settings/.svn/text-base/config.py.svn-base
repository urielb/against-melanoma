
from utils import LOCAL, is_production

ADMINS = (
    ('Uriel Bertoche', 'bertoche.uriel@gmail.com'),
    # ('Uriel Bertoche', 'uriel.bertoche@uniriotec.br'),
    # ('Centro de Tecnologia', 'ct@drderma.com.br'),
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

ROOT_URLCONF = 'urls'

# FOR PIL USE
IMAGE_SIZE = {'width': 800, 'height': 600}
THUMB_SIZE = {'width': 300, 'height': 200}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "drderma.com.br@gmail.com" #'uriel.bertoche@gmail.com' # 'noreply@drderma.com.br'
EMAIL_HOST_PASSWORD = 'RooT147258'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

'''
PAGSEGURO_EMAIL_COBRANCA = 'juliana.m.louback@gmail.com' # email de cobranca usado no pagseguro
PAGSEGURO_TOKEN = 'D31979BD7E63472892441EC43E352752' # '1a3ea7wq2e7eq8e1e223add23ad23' # token gerado no sistema de url de retorno do pagseguro
PAGSEGURO_URL_RETORNO = '/treatments/pagseguro/retorno/' # url para receber o POST de retorno do pagseguro
PAGSEGURO_URL_FINAL = '/treatments/payment_complete/' # url final para redirecionamento
PAGSEGURO_ERRO_LOG  = LOCAL('logs') + '/pagseguro_erro.log' # arquivo para salvar os erros de validacao de retorno com o pagseguro(opcional
'''

FIXTURE_DIRS = (
    LOCAL('fixtures'),
)

MEDIA_ROOT = LOCAL('media') 

# MEDIA_URL = 'http://localhost:8000/drderma/media/'

STATIC_ROOT = LOCAL('static_root')

# SITE_URL = 'http://%s' % DEV_IP

if is_production():
    SITE_URL = 'http://www.drderma.com.br'
else:
    SITE_URL = 'http://127.0.0.1'

MEDIA_URL = '%s/media/' % SITE_URL

#MEDIA_URL = '/media/'

STATIC_URL = '%s/static/' % SITE_URL
STATIC_URL = '/static/'
# STATIC_URL = 'http://localhost:8000/drderma/static/'

STATICFILES_DIRS = (
    LOCAL('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    LOCAL('templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
