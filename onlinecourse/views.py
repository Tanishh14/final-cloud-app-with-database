import logging
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Enrollment, Lesson, Question, Choice, Submission

# Get an instance of a logger
logger = logging.getLogger(__name__)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('psw', '')
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except User.DoesNotExist:
            logger.info("New user registration: %s", username)

        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('psw', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    if user.is_authenticated:
        return Enrollment.objects.filter(user=user, course=course).exists()
    return False


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            course.is_enrolled = check_if_enrolled(user, course)
        else:
            course.is_enrolled = False
        # Gather all questions associated with course or its lessons
        course_questions = list(course.questions.all())
        lesson_questions = list(Question.objects.filter(lesson__course=course))
        seen = set()
        all_questions = []
        for q in course_questions + lesson_questions:
            if q.id not in seen:
                seen.add(q.id)
                all_questions.append(q)
        context['questions'] = all_questions
        return context


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


def extract_answers(request):
    """
    Extract submitted choice IDs from the POST request.
    Handles various naming conventions: choice_<id>, choice, etc.
    """
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            for val in request.POST.getlist(key):
                try:
                    choice_id = int(val)
                    submitted_answers.append(choice_id)
                except (ValueError, TypeError):
                    pass
    return list(set(submitted_answers))


def submit(request, course_id):
    """
    Accepts student mock exam submission, validates input, records Submission,
    and redirects to show_exam_result.
    """
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if not user.is_authenticated:
        return redirect('onlinecourse:login')

    if request.method == 'POST':
        enrollment, _ = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={'mode': 'honor'}
        )
        submitted_choice_ids = extract_answers(request)
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in submitted_choice_ids:
            try:
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('onlinecourse:course_details', pk=course.id)


def show_exam_result(request, course_id, submission_id):
    """
    Retrieves the saved submission attempt, evaluates each question server-side,
    calculates score and grade percentage, and displays the exam result.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Collect questions related to this course
    course_questions = list(course.questions.all())
    lesson_questions = list(Question.objects.filter(lesson__course=course))
    seen = set()
    questions = []
    for q in course_questions + lesson_questions:
        if q.id not in seen:
            seen.add(q.id)
            questions.append(q)

    if not questions:
        questions = list(Question.objects.filter(course=course))

    selected_choice_ids = set(submission.choices.values_list('id', flat=True))

    total_score = 0
    max_score = 0
    question_results = []

    for question in questions:
        q_grade = question.grade if question.grade > 0 else 1
        max_score += q_grade

        is_correct = question.is_get_score(selected_choice_ids)
        if is_correct:
            total_score += q_grade

        choices_detail = []
        for choice in question.choices.all():
            is_selected = choice.id in selected_choice_ids
            choices_detail.append({
                'choice': choice,
                'is_selected': is_selected,
                'is_correct': choice.is_correct,
            })

        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'grade': q_grade if is_correct else 0,
            'max_grade': q_grade,
            'choices_detail': choices_detail,
        })

    grade_percentage = round((total_score / max_score) * 100) if max_score > 0 else 0
    passed = grade_percentage >= 80

    context = {
        'course': course,
        'submission': submission,
        'grade': grade_percentage,
        'score': total_score,
        'max_score': max_score,
        'total_questions': len(questions),
        'question_results': question_results,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
