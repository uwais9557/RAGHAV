"""
Talent Finder - Admin Configuration
=====================================
Customized Django admin panel for managing all models
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Skill, Company, Job, Resume, JobMatch, UserProfile


# ─── Skill Admin ──────────────────────────────────────────────────────────────
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'job_count']
    list_filter = ['category']
    search_fields = ['name']

    def job_count(self, obj):
        return obj.jobs.count()
    job_count.short_description = 'Jobs Requiring This Skill'


# ─── Company Admin ────────────────────────────────────────────────────────────
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'city', 'country', 'rating', 'job_count']
    list_filter = ['industry', 'country']
    search_fields = ['name', 'city']

    def job_count(self, obj):
        return obj.jobs.count()
    job_count.short_description = 'Open Jobs'


# ─── Job Admin ────────────────────────────────────────────────────────────────
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'experience_level', 'job_type', 'location', 'is_active', 'posted_date']
    list_filter = ['is_active', 'experience_level', 'job_type']
    search_fields = ['title', 'company__name', 'description']
    filter_horizontal = ['required_skills']
    list_editable = ['is_active']
    date_hierarchy = 'posted_date'


# ─── Resume Admin ─────────────────────────────────────────────────────────────
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'user', 'file_type', 'ats_score', 'skill_count', 'status', 'uploaded_at']
    list_filter = ['status', 'file_type']
    search_fields = ['user__username', 'original_filename', 'candidate_name']
    readonly_fields = ['uploaded_at', 'analyzed_at', 'extracted_text']

    def skill_count(self, obj):
        return obj.detected_skills.count()
    skill_count.short_description = 'Skills Detected'

    def ats_score_bar(self, obj):
        color = 'green' if obj.ats_score >= 70 else 'orange' if obj.ats_score >= 40 else 'red'
        return format_html(
            '<div style="background:{}; width:{}px; height:10px; border-radius:5px;"></div> {}%',
            color, obj.ats_score, obj.ats_score
        )
    ats_score_bar.short_description = 'ATS Score'


# ─── Job Match Admin ──────────────────────────────────────────────────────────
@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ['resume', 'job', 'match_percentage', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


# ─── User Profile Admin ───────────────────────────────────────────────────────
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'resume_count', 'created_at']
    search_fields = ['user__username', 'user__email']

    def resume_count(self, obj):
        return Resume.objects.filter(user=obj.user).count()
    resume_count.short_description = 'Resumes Uploaded'
