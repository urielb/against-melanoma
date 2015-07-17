from config import SITE_URL
import os

SITE_NAME = SITE_URL

if os.environ.get('CURRENT_ENV', 'DEV') == 'DEV':
    PAYPAL_TEST = True
else:
    PAYPAL_TEST = False           # Testing mode on

if PAYPAL_TEST:
    PAYPAL_RECEIVER_EMAIL = "uriel.bertoche-facilitator@uniriotec.br"
    PAYPAL_WPP_USER = "uriel.bertoche-facilitator_api1.uniriotec.br"      # Get from PayPal
    PAYPAL_WPP_PASSWORD = "1364854286"
    PAYPAL_WPP_SIGNATURE = "A7zAHBbBbsw6a097Vpo.6f8p6YNqAKdXTSqhuNHctUYAoSr2OVrKAVww"
else:
    PAYPAL_RECEIVER_EMAIL = "juliana.louback@uniriotec.br"
    PAYPAL_WPP_USER = "juliana.louback_api1.uniriotec.br"      # Get from PayPal
    PAYPAL_WPP_PASSWORD = "4AC3MWBGC3XMYLLV"
    PAYPAL_WPP_SIGNATURE = "AwU8y-1mmE-lTJZVrk6pS1pIyE90AoBu8qvu5bZFnkwcqip8hsGVo64m"
