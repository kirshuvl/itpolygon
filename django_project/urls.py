from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from crm.lead.views import LandingPage
from users.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('crm/', include('crm.urls')),
    path('', include('cms.urls')),
    path('', include('lms.urls')),
    path('', include('users.urls')),
    path('', HomePage.as_view(), name='HomePage'),
    path('promo/<str:course_slug>', LandingPage.as_view(), name='LandingPage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
