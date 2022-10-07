import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'pR63YVAcFJ7d6UBl1p1RWMuS6LQnI4hNOO3YUYFOLA0q6TsRsO8jzhECytHmKpsa'
DEBUG = False
ALLOWED_HOSTS = ['194.58.111.150', '2a00:f940:2:4:2::4ac8', '194-58-111-150.cloudvps.regruhosting.ru', 'itpolygon.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_project_db',
        'USER': 'django',
        'PASSWORD': 'we9sae9eegie',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'django_project/static'),
]
