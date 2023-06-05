import os
from .settings_ckeditor import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'users.apps.UsersConfig',
    'lms.courses.apps.CoursesConfig',
    'lms.topics.apps.TopicsConfig',
    'lms.lessons.apps.LessonsConfig',
    'lms.steps.apps.StepsConfig',
    'lms.help.apps.OtherConfig',
    'lms.achievements.apps.AchievementsConfig',
    'lms.problems.apps.ProblemsConfig',
    'lms.homeworks.apps.HomeworksConfig',
    'lms.assignment.apps.AssignmentConfig',
    'crm.lead.apps.LeadConfig',
    'cms.other.apps.OtherConfig',
    'cms.constructor.apps.ConstructorConfig',
    #'cms.feedback.apps.FeedbackConfig',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'users.templatetags.users_tags',
                'lms.courses.templatetags.courses_tags',
                'lms.lessons.templatetags.lessons_tags',
                'lms.steps.templatetags.steps_tags',
                'lms.homeworks.templatetags.homeworks_tags',
                'lms.assignment.templatetags.assignment_tags',
            ]
        },

    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'HomePage'
LOGOUT_REDIRECT_URL = 'HomePage'
CKEDITOR_UPLOAD_PATH = 'uploads/'
LOGIN_URL = 'UserLogin'

REDIS_HOST = '0.0.0.0'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

try:
    from .settings_local import *
except ImportError:
    from .settings_production import *
