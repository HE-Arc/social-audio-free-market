from safm_project.settings.common import *

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'https://safmarket.srvz-webapp.he-arc.ch/']

CORS_ORIGIN_WHITELIST = [
    'https://safmarket.srvz-webapp.he-arc.ch/',
]
