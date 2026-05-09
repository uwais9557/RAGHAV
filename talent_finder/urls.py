"""
Talent Finder URL Configuration
================================
Main URL routing for the project
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('talentfinder.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ─── Admin Customization ───────────────────────────────────────────────────────
admin.site.site_header = "Talent Finder Admin"
admin.site.site_title = "Talent Finder"
admin.site.index_title = "Welcome to Talent Finder Administration"
