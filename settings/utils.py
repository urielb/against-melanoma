
import os
LOCAL = lambda x: os.path.join('/'.join(
                os.path.abspath(
                    os.path.dirname(__file__)).split('/')[:-1]), x)
def is_production():
    return os.environ.get('CURRENT_ENV', 'DEV') == 'PROD'
