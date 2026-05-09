# 🎯 Talent Finder — AI Resume Analyzer & Job Recommendation System

> **MCA Final Year Project | Django + Python + AI/ML**

A production-ready Smart Resume Analyzer that uses NLP, TF-IDF, and cosine similarity to extract skills from resumes, calculate ATS scores, and recommend the best job matches from top Indian tech companies.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📄 Multi-Format Parsing | PDF, DOCX, TXT, PNG, JPG via OCR |
| 🧠 AI Skill Detection | 70+ skills detected with NLP keyword matching |
| 📊 ATS Score | 0–100 score based on skills, education, contact info |
| 🎯 Job Matching | TF-IDF cosine similarity + skill overlap scoring |
| 🏢 Company Recommendations | Top matching companies with location & rating |
| 📉 Skill Gap Analysis | Missing skills + Coursera/Udemy course suggestions |
| 📈 Interactive Dashboard | Chart.js doughnut charts and progress bars |
| 🌗 Dark/Light Mode | Persisted via localStorage |
| 🔐 Authentication | Register, Login, Logout with profile page |
| ⚙️ Django Admin | Full CRUD for jobs, companies, resumes, users |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Django 4.2
- **Database:** SQLite3
- **Frontend:** Bootstrap 5, Chart.js, Font Awesome, Custom CSS/JS
- **NLP/ML:** scikit-learn (TF-IDF + Cosine Similarity), NLTK
- **Resume Parsing:** PyPDF2, python-docx, pytesseract + Pillow
- **Fonts:** Syne (headings) + Inter (body)

---

## ⚡ Quick Installation

### Step 1 — Clone & Setup

```bash
# 1. Navigate to project folder
cd talent_finder

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note for pytesseract:** Also install Tesseract OCR binary:
> - **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
> - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
> - **macOS:** `brew install tesseract`

### Step 3 — Database Setup

```bash
# Create database tables
python manage.py makemigrations talentfinder
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser

# Populate sample data (IMPORTANT - run this!)
python manage.py populate_data
```

### Step 4 — Run Development Server

```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
talent_finder/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                    # Auto-created after migrate
├── media/
│   └── resumes/                  # Uploaded resume files
├── talent_finder/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── talentfinder/                 # Main Django app
    ├── models.py                 # Database models
    ├── views.py                  # All view functions
    ├── urls.py                   # URL routes
    ├── forms.py                  # Django forms
    ├── admin.py                  # Admin configuration
    ├── analyzer.py               # AI/NLP resume engine ⭐
    ├── apps.py
    ├── migrations/
    ├── management/
    │   └── commands/
    │       └── populate_data.py  # Sample data seeder
    ├── templates/
    │   └── talentfinder/
    │       ├── base.html         # Base layout
    │       ├── home.html         # Landing page
    │       ├── upload.html       # Resume upload
    │       ├── dashboard.html    # Analysis results
    │       ├── jobs.html         # Job listing
    │       ├── job_detail.html   # Job details
    │       ├── login.html
    │       ├── register.html
    │       ├── profile.html
    │       ├── about.html
    │       └── contact.html
    └── static/
        └── talentfinder/
            ├── css/
            │   └── style.css     # Custom styles
            └── js/
                └── main.js       # JavaScript logic
```

---

## 🔑 Admin Access

After creating superuser:

URL: **http://127.0.0.1:8000/admin/**

From admin you can:
- Add/Edit/Delete Jobs
- Manage Companies
- View uploaded Resumes and scores
- Manage Users and Profiles

---

## 🧠 How the AI Works

### 1. Text Extraction
- **PDF** → PyPDF2 page-by-page text extraction
- **DOCX** → python-docx paragraph + table extraction
- **TXT** → Direct file read with UTF-8 encoding
- **Images** → pytesseract OCR (requires Tesseract binary)

### 2. Skill Detection
Keyword matching with regex word-boundary patterns against a database of 70+ skills across categories: Programming, Web, Frameworks, Databases, Cloud, Data Science, Tools.

### 3. ATS Score Algorithm
```
ATS Score = Skills Score (40%) + Contact Info (20%) + Education (15%) + Experience (15%) + Length (10%)
```

### 4. Job Matching
```
match_pct = (skills_in_common / total_required_skills) × 100
+ TF-IDF cosine_similarity(resume_text, job_description) × 20%
```

Jobs ranked by final score descending. Top 5 saved to `JobMatch` table.

---

## 📸 Pages

| Page | URL | Auth Required |
|---|---|---|
| Home | `/` | ❌ |
| Browse Jobs | `/jobs/` | ❌ |
| Job Detail | `/jobs/<id>/` | ❌ |
| About | `/about/` | ❌ |
| Contact | `/contact/` | ❌ |
| Register | `/register/` | ❌ |
| Login | `/login/` | ❌ |
| Upload Resume | `/upload/` | ✅ |
| Dashboard | `/dashboard/` | ✅ |
| Profile | `/profile/` | ✅ |
| Admin | `/admin/` | ✅ (staff) |

---

## 🎓 Project Info

- **Project Type:** MCA Final Year Project
- **Framework:** Django 4.2
- **Database:** SQLite3
- **AI/ML:** scikit-learn, NLTK
- **Year:** 2024

---

## 💡 Troubleshooting

**pytesseract error:** Install Tesseract binary from https://github.com/UB-Mannheim/tesseract/wiki and add to system PATH.

**No jobs showing:** Run `python manage.py populate_data`

**Static files not loading:** Run `python manage.py collectstatic`

**Migration errors:** Delete `db.sqlite3`, re-run `makemigrations` and `migrate`
