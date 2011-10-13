# Rename this to local_settings.py
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
LOGIN_ERROR_URL = '/login/error/'
#SOCIAL_AUTH_USER_MODEL = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY = 'socialauth_error'

# RabbitMQ configurations
RABBITMQ_CONN = {
    'host': 'localhost'
}
RABBITMQ_QUEUE_NAME = 'campr-queue'

# Override our own settings here, the bare minimum you'll need to specify the
# following
DATABASES = {
    'default': { }
}
MEDIA_ROOT = ''
STATIC_ROOT = ''
STATICFILES_DIRS = ()
SECRET_KEY = ''
TEMPLATE_DIRS = ()
