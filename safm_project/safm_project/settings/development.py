from safm_project.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+y61!gg^qd5%bdee70^oddr=9og5hatc$lq(_i*z^fampo#o9i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('GROUPNAME', 'safm'),
        'USER': os.environ.get('GROUPNAME', 'root'),
        'PASSWORD': os.environ.get('PASSWORD', 'root'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '8889'),
    }
}