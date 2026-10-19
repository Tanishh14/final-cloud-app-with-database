from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Seed database with realistic initial demonstration data for evaluation'

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # 1. Create Superuser 'admin'
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('adminpassword123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"Superuser 'admin' ready (password: adminpassword123)."))

        # 2. Create Student user 'student1'
        student_user, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        student_user.set_password('studentpassword123')
        student_user.save()
        Learner.objects.get_or_create(user=student_user, occupation=Learner.STUDENT)
        self.stdout.write(self.style.SUCCESS(f"Student 'student1' ready (password: studentpassword123)."))

        # 3. Create Instructor
        instructor_user, _ = User.objects.get_or_create(
            username='instructor_jane',
            defaults={
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
            }
        )
        instructor_user.set_password('instructor123')
        instructor_user.save()
        instructor, _ = Instructor.objects.get_or_create(user=instructor_user, defaults={'full_time': True, 'total_learners': 250})

        # 4. Create Course
        course, c_created = Course.objects.get_or_create(
            name="Cloud Application Development with Django and SQL",
            defaults={
                'description': "Master full-stack development with Python, Django ORM, relational databases, and modern cloud deployment patterns.",
                'pub_date': now().date(),
                'total_enrollment': 1,
            }
        )
        course.instructors.add(instructor)
        course.save()
        self.stdout.write(self.style.SUCCESS(f"Course '{course.name}' ready."))

        # 5. Create Lessons
        lessons_data = [
            (
                "Introduction to Cloud Architecture & Django",
                0,
                "In this lesson, we explore cloud web frameworks, MVC/MVT architecture, and the role of Django in building robust, scalable web services."
            ),
            (
                "Django Models, Relational Databases, and ORM",
                1,
                "Learn how Django ORM models map Python objects to SQLite/PostgreSQL relational tables, configure foreign keys, and perform query operations."
            ),
            (
                "Django Admin Interface, Inlines, and Form Security",
                2,
                "Discover how to customize the Django Admin dashboard using ModelAdmin and StackedInline/TabularInline classes, and secure POST requests with CSRF protection."
            ),
        ]

        lessons = []
        for title, order, content in lessons_data:
            lesson, _ = Lesson.objects.get_or_create(
                course=course,
                title=title,
                defaults={'order': order, 'content': content}
            )
            lessons.append(lesson)
        self.stdout.write(self.style.SUCCESS(f"Created {len(lessons)} lessons."))

        # 6. Create 5 Examination Questions with Choices
        # Clear existing questions for clean repeatable run
        Question.objects.filter(course=course).delete()

        exam_data = [
            {
                "text": "Which file in a Django application defines the database schema and model classes?",
                "lesson": lessons[1],
                "grade": 1,
                "choices": [
                    ("models.py", True),
                    ("views.py", False),
                    ("urls.py", False),
                    ("settings.py", False),
                ]
            },
            {
                "text": "Which Django ORM method retrieves all records for a given model from the database?",
                "lesson": lessons[1],
                "grade": 1,
                "choices": [
                    ("Model.objects.all()", True),
                    ("Model.objects.get_all()", False),
                    ("Model.objects.fetch_all()", False),
                    ("Model.select_all()", False),
                ]
            },
            {
                "text": "Which admin class allows child models to be edited vertically directly within a parent model's page?",
                "lesson": lessons[2],
                "grade": 1,
                "choices": [
                    ("admin.StackedInline", True),
                    ("admin.VerticalInline", False),
                    ("admin.BlockInline", False),
                    ("admin.SectionInline", False),
                ]
            },
            {
                "text": "Which HTTP request method must be used when submitting a secure exam form with answers?",
                "lesson": lessons[2],
                "grade": 1,
                "choices": [
                    ("POST", True),
                    ("GET", False),
                    ("HEAD", False),
                    ("OPTIONS", False),
                ]
            },
            {
                "text": "Which Django template tag is required inside an HTML form to protect against Cross-Site Request Forgery?",
                "lesson": lessons[2],
                "grade": 1,
                "choices": [
                    ("{% csrf_token %}", True),
                    ("{% secure_token %}", False),
                    ("{% protect_csrf %}", False),
                    ("{% auth_token %}", False),
                ]
            },
        ]

        for q_data in exam_data:
            q = Question.objects.create(
                course=course,
                lesson=q_data["lesson"],
                question_text=q_data["text"],
                grade=q_data["grade"]
            )
            for choice_text, is_correct in q_data["choices"]:
                Choice.objects.create(
                    question=q,
                    choice_text=choice_text,
                    is_correct=is_correct
                )

        self.stdout.write(self.style.SUCCESS(f"Created {len(exam_data)} exam questions with choices."))

        # 7. Create enrollments
        Enrollment.objects.get_or_create(user=student_user, course=course, defaults={'mode': 'honor'})
        Enrollment.objects.get_or_create(user=admin_user, course=course, defaults={'mode': 'honor'})

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
