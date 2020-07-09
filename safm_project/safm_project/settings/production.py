from safm_project.settings.common import *

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('GROUPNAME', 'safm'),
        'USER': os.environ.get('GROUPNAME', 'root'),
        'PASSWORD': os.environ.get('PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
    }
}

EMAIL_HOST = os.environ.get('SMTP_HOST', 'smtp')
EMAIL_HOST_USER = os.environ.get('GROUPNAME', '')
EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD', '')
EMAIL_PORT = os.environ.get('SMTP_PORT', '2525')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'safmarket.srvz-webapp.he-arc.ch']

CORS_ORIGIN_WHITELIST = [
    'https://safmarket.srvz-webapp.he-arc.ch',
]
