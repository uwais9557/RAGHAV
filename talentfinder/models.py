"""
Talent Finder - Database Models
================================
Models for Resume, Skills, Jobs, Companies, and User Profiles
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ─── Skill Model ──────────────────────────────────────────────────────────────
class Skill(models.Model):
    """Master list of all detectable skills"""
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('web', 'Web Technologies'),
        ('database', 'Database'),
        ('framework', 'Frameworks & Libraries'),
        ('cloud', 'Cloud & DevOps'),
        ('data_science', 'Data Science & AI'),
        ('tools', 'Tools & Software'),
        ('soft', 'Soft Skills'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='programming')
    icon = models.CharField(max_length=50, default='fa-code')  # FontAwesome icon class

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# ─── Company Model ────────────────────────────────────────────────────────────
class Company(models.Model):
    """Companies available for job matching"""
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo_url = models.CharField(max_length=300, blank=True)
    size = models.CharField(max_length=50, blank=True)  # e.g. "1000-5000 employees"
    founded_year = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(default=4.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']


# ─── Job Model ────────────────────────────────────────────────────────────────
class Job(models.Model):
    """Job listings with skill requirements"""
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher (0-1 years)'),
        ('junior', 'Junior (1-3 years)'),
        ('mid', 'Mid-level (3-5 years)'),
        ('senior', 'Senior (5+ years)'),
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    salary_min = models.IntegerField(default=300000)  # Annual in INR
    salary_max = models.IntegerField(default=800000)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)
    apply_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def salary_display(self):
        """Return formatted salary range"""
        return f"₹{self.salary_min//100000:.1f}L - ₹{self.salary_max//100000:.1f}L"

    class Meta:
        ordering = ['-posted_date']


# ─── Resume Model ─────────────────────────────────────────────────────────────
class Resume(models.Model):
    """Uploaded resume files with extracted data"""
    STATUS_CHOICES = [
        ('pending', 'Pending Analysis'),
        ('processing', 'Processing'),
        ('completed', 'Analysis Complete'),
        ('failed', 'Analysis Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20)  # pdf, docx, txt, image

    # Extracted content
    extracted_text = models.TextField(blank=True)
    detected_skills = models.ManyToManyField(Skill, related_name='resumes', blank=True)

    # Analysis results
    ats_score = models.IntegerField(default=0)  # 0-100
    experience_years = models.FloatField(default=0)
    education_level = models.CharField(max_length=100, blank=True)
    candidate_name = models.CharField(max_length=200, blank=True)
    candidate_email = models.CharField(max_length=200, blank=True)
    candidate_phone = models.CharField(max_length=20, blank=True)

    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.original_filename} by {self.user.username}"

    def get_file_size_display(self):
        """Human-readable file size"""
        try:
            size = self.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        except Exception:
            return "Unknown"

    class Meta:
        ordering = ['-uploaded_at']


# ─── Job Match Model ──────────────────────────────────────────────────────────
class JobMatch(models.Model):
    """Stores job recommendation results for each resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_matches')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_percentage = models.FloatField(default=0.0)  # 0-100
    matched_skills = models.ManyToManyField(Skill, related_name='job_matches', blank=True)
    missing_skills = models.TextField(blank=True)  # JSON list of missing skill names
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.original_filename} → {self.job.title} ({self.match_percentage:.1f}%)"

    class Meta:
        ordering = ['-match_percentage']


# ─── User Profile Model ───────────────────────────────────────────────────────
class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    preferred_job_type = models.CharField(max_length=20, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_total_resumes(self):
        return Resume.objects.filter(user=self.user).count()

    def get_latest_resume(self):
        return Resume.objects.filter(user=self.user).first()
