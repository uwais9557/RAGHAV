"""
Talent Finder App URL Patterns
================================
All routes for the talentfinder application
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Public Pages ───────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('jobs/', views.jobs_list, name='jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

    # ── Authentication ─────────────────────────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ── Core Features (Login Required) ────────────────────────────────────────
    path('upload/', views.upload_resume, name='upload_resume'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('resume/delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),

    # ── API Endpoints ──────────────────────────────────────────────────────────
    path('api/resume/status/<int:resume_id>/', views.api_resume_status, name='api_resume_status'),
    path('api/jobs/search/', views.api_jobs_search, name='api_jobs_search'),
]
