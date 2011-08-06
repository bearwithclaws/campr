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

# Override our own settings here
