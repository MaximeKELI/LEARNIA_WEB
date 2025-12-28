"""
URL configuration for learnia project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('tuteur/', include('tutor.urls')),
    path('qcm/', include('qcm.urls')),
    path('flashcards/', include('flashcards.urls')),
    path('resume/', include('resume.urls')),
    path('traduction/', include('translation.urls')),
    path('analyses/', include('analytics.urls')),
    path('planificateur/', include('planner.urls')),
    path('ocr/', include('ocr.urls')),
    path('orientation/', include('orientation.urls')),
    path('export/', include('export.urls')),
    path('gamification/', include('gamification.urls')),
    path('notes/', include('notes.urls')),
    path('calendrier/', include('calendar_app.urls')),
    path('fiches/', include('fiches.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

