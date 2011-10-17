import os

TWITTER_CONSUMER_KEY = 'z3ouiCFSmukouJ7tmcqsw'
TWITTER_CONSUMER_SECRET = 'QHTHuoXT9JxRjlRMSxwz4Nsnv1jb78wicu1UXD1bI'

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

MEDIA_ROOT = os.path.dirname(__file__) + '/media'

STATIC_ROOT = os.path.dirname(__file__) + '/../static'

STATICFILES_DIRS = (os.path.dirname(__file__) + '/static/', )

SECRET_KEY = '^yxvp7d%ek)&!j7s$o4j0mm)@b1+o356l^#s-p9^7cdy$mun4m'

TEMPLATE_DIRS = (
    os.path.dirname(__file__) + '/templates',
)