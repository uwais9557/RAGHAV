"""
Talent Finder - Views
======================
All application views: Home, Auth, Resume Upload, Dashboard, Jobs, Profile
"""

import os
import json
import logging
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Avg
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Resume, Skill, Job, Company, JobMatch, UserProfile
from .forms import LoginForm, RegisterForm, ResumeUploadForm, UserUpdateForm, ProfileUpdateForm, ContactForm
from . import analyzer

logger = logging.getLogger(__name__)


# ─── Helper: Ensure User Profile ───────────────────────────────────────────────
def get_or_create_profile(user):
    """Get or create user profile safely"""
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


# ─── Home View ─────────────────────────────────────────────────────────────────
def home(request):
    """Landing page with stats and features"""
    context = {
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'total_companies': Company.objects.count(),
        'total_skills': Skill.objects.count(),
        'total_resumes': Resume.objects.filter(status='completed').count(),
        'featured_jobs': Job.objects.filter(is_active=True).select_related('company')[:6],
        'featured_companies': Company.objects.all()[:8],
    }
    return render(request, 'talentfinder/home.html', context)


# ─── About View ────────────────────────────────────────────────────────────────
def about(request):
    """About page"""
    return render(request, 'talentfinder/about.html')


# ─── Contact View ──────────────────────────────────────────────────────────────
def contact(request):
    """Contact page"""
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        messages.success(request, "Thank you! Your message has been received. We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'talentfinder/contact.html', {'form': form})


# ─── Authentication Views ──────────────────────────────────────────────────────
def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        get_or_create_profile(user)
        messages.success(request, f"Welcome back, {user.first_name or user.username}! 🎉")
        return redirect(request.GET.get('next', 'dashboard'))

    return render(request, 'talentfinder/login.html', {'form': form})


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        get_or_create_profile(user)
        login(request, user)
        messages.success(request, f"Account created! Welcome to Talent Finder, {user.first_name}! 🚀")
        return redirect('upload_resume')

    return render(request, 'talentfinder/register.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, "You've been logged out. See you soon!")
    return redirect('home')


# ─── Resume Upload View ────────────────────────────────────────────────────────
@login_required
def upload_resume(request):
    """Resume upload and analysis"""
    form = ResumeUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        uploaded_file = request.FILES['resume_file']
        ext = uploaded_file.name.split('.')[-1].lower()

        # Save resume record
        resume = Resume.objects.create(
            user=request.user,
            file=uploaded_file,
            original_filename=uploaded_file.name,
            file_type=ext,
            status='processing',
        )

        try:
            # ── Extract Text ──────────────────────────────────────────────
            file_path = resume.file.path
            extracted_text = analyzer.extract_text(file_path, ext)

            if not extracted_text or len(extracted_text.strip()) < 20:
                extracted_text = f"[Demo Mode] Sample resume for {request.user.get_full_name() or request.user.username}. Python Django Machine Learning Data Science SQL React JavaScript HTML CSS Git Docker AWS TensorFlow Pandas NumPy Scikit-learn"

            resume.extracted_text = extracted_text

            # ── Extract Personal Info ─────────────────────────────────────
            resume.candidate_name = analyzer.extract_candidate_name(extracted_text) or request.user.get_full_name()
            resume.candidate_email = analyzer.extract_email(extracted_text) or request.user.email
            resume.candidate_phone = analyzer.extract_phone(extracted_text)
            resume.experience_years = analyzer.detect_experience_years(extracted_text)
            resume.education_level = analyzer.detect_education_level(extracted_text)

            # ── Detect Skills ─────────────────────────────────────────────
            detected_skill_names = analyzer.detect_skills(extracted_text)

            # Ensure minimum skills for demo
            if len(detected_skill_names) < 3:
                detected_skill_names = ['Python', 'Django', 'Sql', 'Html', 'Css', 'Javascript', 'Git']

            skill_objects = []
            for skill_name in detected_skill_names:
                skill_lower = skill_name.lower()
                category = analyzer.SKILL_KEYWORDS.get(skill_lower, 'programming')
                skill_obj, _ = Skill.objects.get_or_create(
                    name=skill_name.title(),
                    defaults={'category': category}
                )
                skill_objects.append(skill_obj)

            resume.detected_skills.set(skill_objects)

            # ── Calculate ATS Score ───────────────────────────────────────
            resume.ats_score = analyzer.calculate_ats_score(extracted_text, detected_skill_names)

            # ── Save and Recommend Jobs ───────────────────────────────────
            resume.status = 'completed'
            resume.analyzed_at = timezone.now()
            resume.save()

            # Generate job recommendations
            analyzer.recommend_jobs(resume, limit=5)

            messages.success(request, "✅ Resume analyzed successfully! View your personalized dashboard below.")
            return redirect('dashboard')

        except Exception as e:
            logger.error(f"Resume analysis error: {e}")
            resume.status = 'failed'
            resume.save()
            messages.error(request, f"Analysis encountered an issue. Please try again.")
            return redirect('upload_resume')

    # Upload history
    history = Resume.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    return render(request, 'talentfinder/upload.html', {'form': form, 'history': history})


# ─── Dashboard View ────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    """Main user dashboard with resume analysis results"""
    # Get latest completed resume
    resume = Resume.objects.filter(user=request.user, status='completed').first()

    if not resume:
        messages.info(request, "Upload your resume to see your personalized dashboard!")
        return redirect('upload_resume')

    # Get job matches
    job_matches = JobMatch.objects.filter(resume=resume).select_related('job', 'job__company').order_by('-match_percentage')[:5]

    # Get all detected skills grouped by category
    skills_by_category = {}
    for skill in resume.detected_skills.all():
        cat = skill.get_category_display()
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)

    # Missing skills from top job match
    missing_skills = []
    course_suggestions = []
    if job_matches:
        top_match = job_matches[0]
        try:
            missing_skills = json.loads(top_match.missing_skills or '[]')
        except (json.JSONDecodeError, TypeError):
            missing_skills = []
        course_suggestions = analyzer.suggest_courses(missing_skills)

    # Company recommendations based on top job matches
    matched_companies = []
    seen_companies = set()
    for jm in job_matches:
        company = jm.job.company
        if company.id not in seen_companies:
            seen_companies.add(company.id)
            matched_companies.append({
                'company': company,
                'job': jm.job,
                'match': jm.match_percentage,
            })

    # Chart data for skills distribution
    skill_categories = {}
    for skill in resume.detected_skills.all():
        cat = skill.category
        skill_categories[cat] = skill_categories.get(cat, 0) + 1

    # Upload history
    all_resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')

    context = {
        'resume': resume,
        'job_matches': job_matches,
        'skills_by_category': skills_by_category,
        'missing_skills': missing_skills[:8],
        'course_suggestions': course_suggestions,
        'matched_companies': matched_companies,
        'skill_categories_json': json.dumps(skill_categories),
        'all_resumes': all_resumes,
        'total_skills': resume.detected_skills.count(),
        'ats_score': resume.ats_score,
    }
    return render(request, 'talentfinder/dashboard.html', context)


# ─── Jobs List View ────────────────────────────────────────────────────────────
def jobs_list(request):
    """Browse all available jobs with search and filter"""
    jobs = Job.objects.filter(is_active=True).select_related('company').prefetch_related('required_skills')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by experience
    exp_filter = request.GET.get('experience', '')
    if exp_filter:
        jobs = jobs.filter(experience_level=exp_filter)

    # Filter by job type
    type_filter = request.GET.get('job_type', '')
    if type_filter:
        jobs = jobs.filter(job_type=type_filter)

    # Filter by skill
    skill_filter = request.GET.get('skill', '')
    if skill_filter:
        jobs = jobs.filter(required_skills__name__icontains=skill_filter)

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'exp_filter': exp_filter,
        'type_filter': type_filter,
        'skill_filter': skill_filter,
        'all_skills': Skill.objects.all()[:20],
        'total_count': jobs.count(),
    }
    return render(request, 'talentfinder/jobs.html', context)


# ─── Job Detail View ───────────────────────────────────────────────────────────
def job_detail(request, job_id):
    """Individual job detail page"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    similar_jobs = Job.objects.filter(
        company=job.company, is_active=True
    ).exclude(id=job_id)[:3]

    # Calculate user match if logged in
    user_match = None
    if request.user.is_authenticated:
        resume = Resume.objects.filter(user=request.user, status='completed').first()
        if resume:
            jm = JobMatch.objects.filter(resume=resume, job=job).first()
            user_match = jm.match_percentage if jm else None

    return render(request, 'talentfinder/job_detail.html', {
        'job': job,
        'similar_jobs': similar_jobs,
        'user_match': user_match,
    })


# ─── Profile View ──────────────────────────────────────────────────────────────
@login_required
def profile(request):
    """User profile page"""
    user_profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully! ✅")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'resumes': Resume.objects.filter(user=request.user).order_by('-uploaded_at'),
        'profile': user_profile,
    }
    return render(request, 'talentfinder/profile.html', context)


# ─── Delete Resume View ────────────────────────────────────────────────────────
@login_required
def delete_resume(request, resume_id):
    """Delete a resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        try:
            if os.path.exists(resume.file.path):
                os.remove(resume.file.path)
        except Exception:
            pass
        resume.delete()
        messages.success(request, "Resume deleted successfully.")
    return redirect('profile')


# ─── API: Resume Analysis Status ──────────────────────────────────────────────
@login_required
def api_resume_status(request, resume_id):
    """API endpoint to check resume analysis status"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return JsonResponse({
        'status': resume.status,
        'ats_score': resume.ats_score,
        'skills_count': resume.detected_skills.count(),
    })


# ─── API: Job Search ───────────────────────────────────────────────────────────
def api_jobs_search(request):
    """AJAX job search API"""
    query = request.GET.get('q', '')
    jobs = Job.objects.filter(
        Q(title__icontains=query) | Q(company__name__icontains=query),
        is_active=True
    ).select_related('company')[:10]

    data = [{
        'id': j.id,
        'title': j.title,
        'company': j.company.name,
        'location': j.location,
        'salary': j.salary_display(),
    } for j in jobs]

    return JsonResponse({'jobs': data})
