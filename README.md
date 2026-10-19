# OnlineCourse LMS - Django Final Project

A full-stack Learning Management System (LMS) web application developed with **Django**, **Python**, **SQLite**, **HTML5**, and **Bootstrap**. This project implements course catalog browsing, lesson navigation, multiple-choice quiz/exam evaluation, and administration management.

---

## Deliverables & Architecture Overview

| Task | File | Description |
|------|------|-------------|
| **Task 1: Models** | `onlinecourse/models.py` | Models for `Question`, `Choice`, and `Submission` alongside `Course`, `Lesson`, `Instructor`, `Learner`, and `Enrollment`. Implements `is_get_score(selected_ids)` evaluation. |
| **Task 2: Admin** | `onlinecourse/admin.py` | Custom administration interface with 7 models imported, `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, and `LessonAdmin`. |
| **Task 3: Admin Screenshot** | `screenshots/03-admin-site.png` | Screenshot of the running Django admin dashboard displaying both Authentication & Authorization and Onlinecourse. |
| **Task 4: Course Detail Template** | `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` | Responsive Bootstrap template rendering course name, lesson contents, lesson review questions, and exam form. |
| **Task 5: Views** | `onlinecourse/views.py` | `submit` and `show_exam_result` views handling answer extraction, server-side grading, and submission persistence. |
| **Task 6: URLs** | `onlinecourse/urls.py` | Named URL patterns for course list, course details, enroll, submit, and exam result display. |
| **Task 7: Final Screenshot** | `screenshots/07-final.png` | Screenshot of the successful 5/5 exam result page displaying **Congratulations** and detailed answer breakdown. |

---

## Quick Start on Windows

### 1. Prerequisites
- Python 3.10+ installed
- PowerShell / Command Prompt

### 2. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 3. Apply Database Migrations
```powershell
python manage.py makemigrations onlinecourse
python manage.py migrate
```

### 4. Seed Demonstration Data & Create Superuser
Execute the automated management command:
```powershell
python manage.py seed_data
```
This automatically sets up:
- **Superuser**: `admin` / Password: `adminpassword123`
- **Student User**: `student1` / Password: `studentpassword123`
- **Sample Course**: *Cloud Application Development with Django and SQL*
- **3 Lessons**: Structured curriculum content
- **5 Examination Questions**: Real quiz questions with choices

### 5. Run Automated Tests & System Checks
```powershell
python manage.py check
python manage.py test onlinecourse
```

### 6. Start the Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```
Open your browser and navigate to:
- **Application Home**: [http://127.0.0.1:8000/onlinecourse/](http://127.0.0.1:8000/onlinecourse/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Capturing Required Screenshots

### Screenshot 1 (`screenshots/03-admin-site.png`):
1. Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
2. Log in using `admin` / `adminpassword123`.
3. Verify both sections are visible:
   - **Authentication and Authorization** (Groups, Users)
   - **Onlinecourse** (Courses, Lessons, Instructors, Learners, Questions, Choices, Submissions)
4. Take a screenshot and save it as `screenshots/03-admin-site.png`.

### Screenshot 2 (`screenshots/07-final.png`):
1. Navigate to [http://127.0.0.1:8000/onlinecourse/](http://127.0.0.1:8000/onlinecourse/)
2. Log in using `student1` / `studentpassword123` (or `admin` / `adminpassword123`).
3. Click on the course **Cloud Application Development with Django and SQL**.
4. Scroll to the **Course Examination** section and select the correct answers for all 5 questions:
   - Q1: `models.py`
   - Q2: `Model.objects.all()`
   - Q3: `admin.StackedInline`
   - Q4: `POST`
   - Q5: `{% csrf_token %}`
5. Click **Submit Exam**.
6. The results page will render showing **Congratulations!**, score **5/5** (100%), and the question review.
7. Capture the screen and save it as `screenshots/07-final.png`.

---

## GitHub Submission Instructions

To push this repository to your GitHub account:

```powershell
# 1. Stage all project files
git add .

# 2. Commit the changes
git commit -m "Complete Django OnlineCourse LMS final project"

# 3. Rename default branch to main (if not already main)
git branch -M main

# 4. Add your GitHub remote repository URL
git remote set-url origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
# (Or if adding fresh remote: git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git)

# 5. Push to GitHub
git push -u origin main
```

### Verified File URLs (replace with your repository once pushed):
- `models.py`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/onlinecourse/models.py`
- `admin.py`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/onlinecourse/admin.py`
- `course_details_bootstrap.html`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- `views.py`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/onlinecourse/views.py`
- `urls.py`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/onlinecourse/urls.py`
- `README.md`: `https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/blob/main/README.md`
