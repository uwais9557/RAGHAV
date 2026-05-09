"""
Management Command: populate_data
==================================
Seeds the database with sample companies, jobs, and skills
for demonstration purposes.

Usage: python manage.py populate_data
"""

from django.core.management.base import BaseCommand
from talentfinder.models import Skill, Company, Job


class Command(BaseCommand):
    help = 'Populate database with sample skills, companies, and jobs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('🌱 Seeding database with sample data...'))
        self._create_skills()
        self._create_companies()
        self._create_jobs()
        self.stdout.write(self.style.SUCCESS('✅ Database populated successfully!'))

    def _create_skills(self):
        """Create master skill list"""
        skills_data = [
            # Programming Languages
            ('Python', 'programming'), ('Java', 'programming'), ('JavaScript', 'programming'),
            ('C++', 'programming'), ('C#', 'programming'), ('PHP', 'programming'),
            ('Ruby', 'programming'), ('Swift', 'programming'), ('Kotlin', 'programming'),
            ('TypeScript', 'programming'), ('Go', 'programming'), ('R', 'programming'),

            # Web
            ('HTML', 'web'), ('CSS', 'web'), ('React', 'web'), ('Angular', 'web'),
            ('Vue', 'web'), ('Nodejs', 'web'), ('Bootstrap', 'web'), ('jQuery', 'web'),
            ('Next.Js', 'web'), ('Graphql', 'web'), ('Rest Api', 'web'),

            # Frameworks
            ('Django', 'framework'), ('Flask', 'framework'), ('Spring Boot', 'framework'),
            ('Express', 'framework'), ('Flutter', 'framework'), ('React Native', 'framework'),

            # Database
            ('Sql', 'database'), ('Mysql', 'database'), ('Postgresql', 'database'),
            ('Mongodb', 'database'), ('Redis', 'database'), ('Sqlite', 'database'),
            ('Firebase', 'database'), ('Elasticsearch', 'database'),

            # Data Science & AI
            ('Machine Learning', 'data_science'), ('Deep Learning', 'data_science'),
            ('Artificial Intelligence', 'data_science'), ('Data Science', 'data_science'),
            ('Tensorflow', 'data_science'), ('Pytorch', 'data_science'), ('Keras', 'data_science'),
            ('Scikit-Learn', 'data_science'), ('Pandas', 'data_science'), ('Numpy', 'data_science'),
            ('Nlp', 'data_science'), ('Computer Vision', 'data_science'),
            ('Data Analysis', 'data_science'), ('Data Visualization', 'data_science'),

            # Cloud & DevOps
            ('Aws', 'cloud'), ('Azure', 'cloud'), ('Google Cloud', 'cloud'),
            ('Docker', 'cloud'), ('Kubernetes', 'cloud'), ('Jenkins', 'cloud'),
            ('Devops', 'cloud'), ('Ci/Cd', 'cloud'), ('Terraform', 'cloud'),

            # Tools
            ('Git', 'tools'), ('Github', 'tools'), ('Linux', 'tools'),
            ('Power Bi', 'tools'), ('Tableau', 'tools'), ('Excel', 'tools'),
            ('Jira', 'tools'), ('Figma', 'tools'), ('Postman', 'tools'),
            ('Agile', 'tools'), ('Scrum', 'tools'),

            # Mobile
            ('Android', 'programming'), ('Ios', 'programming'),
        ]

        created_count = 0
        for name, category in skills_data:
            _, created = Skill.objects.get_or_create(name=name, defaults={'category': category})
            if created:
                created_count += 1

        self.stdout.write(f'  ✓ Created {created_count} new skills ({Skill.objects.count()} total)')

    def _create_companies(self):
        """Create sample Indian and global tech companies"""
        companies_data = [
            {
                'name': 'Tata Consultancy Services',
                'industry': 'IT Services',
                'location': 'Mumbai, Maharashtra, India',
                'city': 'Mumbai',
                'country': 'India',
                'latitude': 19.0760,
                'longitude': 72.8777,
                'website': 'https://www.tcs.com',
                'description': 'TCS is a global leader in IT services, consulting and business solutions.',
                'size': '500,000+ employees',
                'founded_year': 1968,
                'rating': 4.1,
            },
            {
                'name': 'Infosys',
                'industry': 'IT Services',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://www.infosys.com',
                'description': 'Infosys is a global leader in next-generation digital services and consulting.',
                'size': '350,000+ employees',
                'founded_year': 1981,
                'rating': 4.0,
            },
            {
                'name': 'Wipro Technologies',
                'industry': 'IT Services',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://www.wipro.com',
                'description': 'Wipro is a leading global information technology, consulting and business process services company.',
                'size': '250,000+ employees',
                'founded_year': 1945,
                'rating': 3.9,
            },
            {
                'name': 'HCL Technologies',
                'industry': 'IT Services',
                'location': 'Noida, Uttar Pradesh, India',
                'city': 'Noida',
                'country': 'India',
                'latitude': 28.5355,
                'longitude': 77.3910,
                'website': 'https://www.hcltech.com',
                'description': 'HCL Technologies is a next-generation global technology company.',
                'size': '220,000+ employees',
                'founded_year': 1976,
                'rating': 3.8,
            },
            {
                'name': 'Tech Mahindra',
                'industry': 'IT Services',
                'location': 'Pune, Maharashtra, India',
                'city': 'Pune',
                'country': 'India',
                'latitude': 18.5204,
                'longitude': 73.8567,
                'website': 'https://www.techmahindra.com',
                'description': 'Tech Mahindra offers innovative and customer-centric digital experiences.',
                'size': '150,000+ employees',
                'founded_year': 1986,
                'rating': 3.8,
            },
            {
                'name': 'Google India',
                'industry': 'Technology',
                'location': 'Hyderabad, Telangana, India',
                'city': 'Hyderabad',
                'country': 'India',
                'latitude': 17.3850,
                'longitude': 78.4867,
                'website': 'https://careers.google.com',
                'description': 'Google India development center working on global products.',
                'size': '5,000+ employees',
                'founded_year': 2004,
                'rating': 4.8,
            },
            {
                'name': 'Microsoft India',
                'industry': 'Technology',
                'location': 'Hyderabad, Telangana, India',
                'city': 'Hyderabad',
                'country': 'India',
                'latitude': 17.3850,
                'longitude': 78.4867,
                'website': 'https://careers.microsoft.com',
                'description': 'Microsoft India R&D center, one of the largest outside the US.',
                'size': '10,000+ employees',
                'founded_year': 1990,
                'rating': 4.7,
            },
            {
                'name': 'Amazon India',
                'industry': 'E-Commerce & Cloud',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://www.amazon.jobs',
                'description': 'Amazon India development center for global e-commerce and AWS solutions.',
                'size': '60,000+ employees',
                'founded_year': 2004,
                'rating': 4.3,
            },
            {
                'name': 'Flipkart',
                'industry': 'E-Commerce',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://www.flipkartcareers.com',
                'description': "India's leading e-commerce marketplace with cutting-edge technology.",
                'size': '30,000+ employees',
                'founded_year': 2007,
                'rating': 4.2,
            },
            {
                'name': 'Razorpay',
                'industry': 'Fintech',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://razorpay.com/jobs/',
                'description': "India's leading payments solution provider and neobank.",
                'size': '2,500+ employees',
                'founded_year': 2014,
                'rating': 4.4,
            },
            {
                'name': 'Zomato',
                'industry': 'Food Tech',
                'location': 'Gurugram, Haryana, India',
                'city': 'Gurugram',
                'country': 'India',
                'latitude': 28.4595,
                'longitude': 77.0266,
                'website': 'https://www.zomato.com/careers',
                'description': 'Food delivery and restaurant discovery platform with 25+ countries presence.',
                'size': '10,000+ employees',
                'founded_year': 2008,
                'rating': 3.9,
            },
            {
                'name': 'Ola',
                'industry': 'Mobility Tech',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://www.ola.money/careers',
                'description': "India's largest mobility platform serving 250+ cities.",
                'size': '8,000+ employees',
                'founded_year': 2010,
                'rating': 3.8,
            },
            {
                'name': 'IBM India',
                'industry': 'Technology',
                'location': 'Chennai, Tamil Nadu, India',
                'city': 'Chennai',
                'country': 'India',
                'latitude': 13.0827,
                'longitude': 80.2707,
                'website': 'https://www.ibm.com/employment/',
                'description': 'IBM India is one of the largest IBM operations outside the USA.',
                'size': '120,000+ employees',
                'founded_year': 1992,
                'rating': 4.0,
            },
            {
                'name': 'Accenture India',
                'industry': 'Consulting & IT',
                'location': 'Mumbai, Maharashtra, India',
                'city': 'Mumbai',
                'country': 'India',
                'latitude': 19.0760,
                'longitude': 72.8777,
                'website': 'https://www.accenture.com/in-en/careers',
                'description': 'Global professional services company with leading capabilities in digital, cloud and security.',
                'size': '300,000+ employees in India',
                'founded_year': 2001,
                'rating': 4.1,
            },
            {
                'name': 'BYJU\'S',
                'industry': 'EdTech',
                'location': 'Bangalore, Karnataka, India',
                'city': 'Bangalore',
                'country': 'India',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'website': 'https://byjus.com/careers/',
                'description': "India's largest ed-tech company and world's most valuable ed-tech startup.",
                'size': '25,000+ employees',
                'founded_year': 2011,
                'rating': 3.5,
            },
        ]

        created_count = 0
        for data in companies_data:
            _, created = Company.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                created_count += 1

        self.stdout.write(f'  ✓ Created {created_count} new companies ({Company.objects.count()} total)')

    def _create_jobs(self):
        """Create sample job listings"""
        def get_skills(*names):
            skills = []
            for name in names:
                try:
                    skills.append(Skill.objects.get(name=name))
                except Skill.DoesNotExist:
                    pass
            return skills

        jobs_data = [
            # TCS Jobs
            {
                'company': 'Tata Consultancy Services',
                'title': 'Python Developer',
                'description': 'We are looking for an experienced Python developer to join our growing team. You will be responsible for building and maintaining backend services, APIs, and data pipelines. Experience with Django or Flask is a plus.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 500000,
                'salary_max': 900000,
                'location': 'Mumbai / Bangalore / Pune (Hybrid)',
                'skills': ['Python', 'Django', 'Sql', 'Mysql', 'Git', 'Rest Api'],
            },
            {
                'company': 'Tata Consultancy Services',
                'title': 'Data Analyst',
                'description': 'Join our analytics team to drive data-driven business decisions. You will analyze large datasets, build dashboards, and present insights to stakeholders. Experience with Power BI or Tableau preferred.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 450000,
                'salary_max': 800000,
                'location': 'Chennai / Hyderabad',
                'skills': ['Python', 'Sql', 'Excel', 'Power Bi', 'Data Analysis', 'Pandas'],
            },
            # Infosys Jobs
            {
                'company': 'Infosys',
                'title': 'Full Stack Developer',
                'description': 'Build end-to-end web applications using modern technologies. You will work on both frontend (React/Angular) and backend (Node.js/Java) development in an agile environment.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 700000,
                'salary_max': 1400000,
                'location': 'Bangalore / Pune',
                'skills': ['React', 'Nodejs', 'Javascript', 'Html', 'Css', 'Mongodb', 'Git'],
            },
            {
                'company': 'Infosys',
                'title': 'Java Backend Developer',
                'description': 'Develop robust backend systems using Java and Spring Boot framework. Work on microservices architecture, RESTful APIs, and cloud deployments on AWS.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 800000,
                'salary_max': 1600000,
                'location': 'Hyderabad / Pune',
                'skills': ['Java', 'Spring Boot', 'Sql', 'Aws', 'Docker', 'Rest Api', 'Git'],
            },
            # Google India Jobs
            {
                'company': 'Google India',
                'title': 'Machine Learning Engineer',
                'description': 'Build and deploy ML models at scale. Work on cutting-edge AI/ML projects for Google products used by billions worldwide. Strong background in deep learning frameworks required.',
                'experience_level': 'senior',
                'job_type': 'full_time',
                'salary_min': 2500000,
                'salary_max': 5000000,
                'location': 'Hyderabad / Bangalore',
                'skills': ['Python', 'Machine Learning', 'Deep Learning', 'Tensorflow', 'Pytorch', 'Kubernetes', 'Aws'],
            },
            {
                'company': 'Google India',
                'title': 'Software Engineer - Fresher',
                'description': 'Join Google as a Software Engineer in our Bangalore office. Work on impactful products used globally. Strong algorithmic thinking and coding skills required.',
                'experience_level': 'fresher',
                'job_type': 'full_time',
                'salary_min': 1800000,
                'salary_max': 2800000,
                'location': 'Hyderabad',
                'skills': ['Python', 'Java', 'Data Structures', 'Git', 'Sql'],
            },
            # Microsoft India Jobs
            {
                'company': 'Microsoft India',
                'title': 'Cloud Solutions Engineer',
                'description': 'Design and implement cloud architecture solutions on Microsoft Azure. Work with enterprise clients to migrate workloads and build cloud-native applications.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 1500000,
                'salary_max': 2800000,
                'location': 'Hyderabad',
                'skills': ['Azure', 'Python', 'Docker', 'Kubernetes', 'Devops', 'Sql', 'Rest Api'],
            },
            {
                'company': 'Microsoft India',
                'title': 'Data Engineer',
                'description': 'Build and maintain data pipelines, data lakes, and ETL processes on Azure. Work with massive datasets and collaborate with data scientists and analysts.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 1200000,
                'salary_max': 2200000,
                'location': 'Hyderabad',
                'skills': ['Python', 'Sql', 'Azure', 'Pandas', 'Spark', 'Postgresql', 'Data Analysis'],
            },
            # Amazon India Jobs
            {
                'company': 'Amazon India',
                'title': 'SDE-1 (Software Development Engineer)',
                'description': 'Join Amazon as an SDE-1 and work on building world-class e-commerce and cloud solutions. You will own your features end-to-end from design to deployment.',
                'experience_level': 'fresher',
                'job_type': 'full_time',
                'salary_min': 1600000,
                'salary_max': 2400000,
                'location': 'Bangalore / Hyderabad',
                'skills': ['Python', 'Java', 'Aws', 'Sql', 'Rest Api', 'Git', 'Docker'],
            },
            # Flipkart Jobs
            {
                'company': 'Flipkart',
                'title': 'Android Developer',
                'description': 'Build and enhance Flipkart\'s Android application used by 300 million+ users. Work with modern Android architecture patterns, Kotlin, and Jetpack Compose.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 900000,
                'salary_max': 1600000,
                'location': 'Bangalore',
                'skills': ['Android', 'Kotlin', 'Java', 'Rest Api', 'Git', 'Firebase'],
            },
            {
                'company': 'Flipkart',
                'title': 'Data Scientist',
                'description': 'Apply machine learning and statistical modeling to solve complex business problems in supply chain, pricing, recommendations, and fraud detection.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'location': 'Bangalore',
                'skills': ['Python', 'Machine Learning', 'Data Science', 'Scikit-Learn', 'Pandas', 'Sql', 'Tableau'],
            },
            # Razorpay Jobs
            {
                'company': 'Razorpay',
                'title': 'Backend Engineer',
                'description': 'Build scalable payment infrastructure serving millions of transactions daily. Work on high-availability systems using Go, Python, and microservices architecture.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 1000000,
                'salary_max': 2000000,
                'location': 'Bangalore (Hybrid)',
                'skills': ['Python', 'Sql', 'Redis', 'Docker', 'Rest Api', 'Git', 'Postgresql'],
            },
            # HCL Jobs
            {
                'company': 'HCL Technologies',
                'title': 'DevOps Engineer',
                'description': 'Implement CI/CD pipelines, automate infrastructure provisioning, and manage cloud deployments. Work with Kubernetes, Terraform, Jenkins, and major cloud platforms.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 500000,
                'salary_max': 1000000,
                'location': 'Noida / Pune',
                'skills': ['Devops', 'Docker', 'Kubernetes', 'Jenkins', 'Aws', 'Linux', 'Python', 'Git'],
            },
            {
                'company': 'HCL Technologies',
                'title': 'UI/UX Frontend Developer',
                'description': 'Create beautiful, accessible, and performant user interfaces for enterprise web applications. Collaborate with designers and backend teams.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 450000,
                'salary_max': 850000,
                'location': 'Noida / Chennai',
                'skills': ['React', 'Javascript', 'Html', 'Css', 'Bootstrap', 'Figma', 'Git'],
            },
            # Internships
            {
                'company': 'BYJU\'S',
                'title': 'Python Intern - Backend',
                'description': 'Join our engineering team as an intern and gain hands-on experience building educational technology products. Perfect for final-year students.',
                'experience_level': 'fresher',
                'job_type': 'internship',
                'salary_min': 180000,
                'salary_max': 300000,
                'location': 'Bangalore (WFH)',
                'skills': ['Python', 'Django', 'Html', 'Css', 'Javascript', 'Sql', 'Git'],
            },
            {
                'company': 'Zomato',
                'title': 'Data Science Intern',
                'description': 'Work with our data team to analyze user behavior, build recommendation systems, and improve our food ordering experience through ML.',
                'experience_level': 'fresher',
                'job_type': 'internship',
                'salary_min': 200000,
                'salary_max': 350000,
                'location': 'Gurugram / Remote',
                'skills': ['Python', 'Machine Learning', 'Pandas', 'Numpy', 'Sql', 'Data Analysis'],
            },
            # Remote Jobs
            {
                'company': 'Wipro Technologies',
                'title': 'React.js Developer (Remote)',
                'description': 'Remote opportunity to work on large-scale SaaS products. Build reusable component libraries, optimize performance, and mentor junior developers.',
                'experience_level': 'mid',
                'job_type': 'remote',
                'salary_min': 800000,
                'salary_max': 1600000,
                'location': 'Remote (Pan India)',
                'skills': ['React', 'Javascript', 'TypeScript', 'Html', 'Css', 'Rest Api', 'Git'],
            },
            {
                'company': 'Accenture India',
                'title': 'NLP / AI Research Engineer',
                'description': 'Research and develop Natural Language Processing solutions for enterprise clients. Build production NLP pipelines, chatbots, and document intelligence systems.',
                'experience_level': 'senior',
                'job_type': 'full_time',
                'salary_min': 1500000,
                'salary_max': 2800000,
                'location': 'Bangalore / Hyderabad',
                'skills': ['Python', 'Nlp', 'Machine Learning', 'Deep Learning', 'Tensorflow', 'Pytorch', 'Scikit-Learn'],
            },
            {
                'company': 'IBM India',
                'title': 'Database Administrator',
                'description': 'Manage, monitor, and optimize enterprise databases. Work with Oracle, PostgreSQL, and cloud databases. Ensure high availability and data security.',
                'experience_level': 'mid',
                'job_type': 'full_time',
                'salary_min': 700000,
                'salary_max': 1200000,
                'location': 'Chennai / Bangalore',
                'skills': ['Sql', 'Postgresql', 'Mysql', 'Oracle', 'Linux', 'Python', 'Elasticsearch'],
            },
            {
                'company': 'Ola',
                'title': 'Flutter Mobile Developer',
                'description': 'Build cross-platform mobile applications using Flutter. Create seamless user experiences for our ride-hailing and electric vehicle apps.',
                'experience_level': 'junior',
                'job_type': 'full_time',
                'salary_min': 700000,
                'salary_max': 1400000,
                'location': 'Bangalore',
                'skills': ['Flutter', 'Dart', 'Android', 'Ios', 'Rest Api', 'Firebase', 'Git'],
            },
        ]

        created_count = 0
        for job_data in jobs_data:
            company_name = job_data.pop('company')
            skill_names = job_data.pop('skills')

            try:
                company = Company.objects.get(name=company_name)
                job, created = Job.objects.get_or_create(
                    title=job_data['title'],
                    company=company,
                    defaults=job_data
                )
                if created:
                    # Add skills
                    for skill_name in skill_names:
                        try:
                            skill = Skill.objects.get(name=skill_name)
                            job.required_skills.add(skill)
                        except Skill.DoesNotExist:
                            pass
                    created_count += 1
            except Company.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Company not found: {company_name}'))

        self.stdout.write(f'  ✓ Created {created_count} new jobs ({Job.objects.count()} total)')
