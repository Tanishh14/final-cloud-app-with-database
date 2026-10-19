from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin
from onlinecourse.models import Course, Lesson, Question, Choice, Submission, Enrollment
from onlinecourse.admin import QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin


class OnlineCourseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='testpassword')
        self.course = Course.objects.create(name='Test Course', description='Test Description')
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, content='Test Content')
        self.question = Question.objects.create(
            lesson=self.lesson,
            course=self.course,
            question_text='What is Django?',
            grade=1
        )
        self.c1 = Choice.objects.create(question=self.question, choice_text='A Python web framework', is_correct=True)
        self.c2 = Choice.objects.create(question=self.question, choice_text='A database', is_correct=False)
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)

    def test_question_choice_relationship(self):
        self.assertEqual(self.question.choices.count(), 2)
        self.assertEqual(self.question.lesson, self.lesson)
        self.assertEqual(self.question.course, self.course)

    def test_is_get_score(self):
        # Correct choice selected
        self.assertTrue(self.question.is_get_score([self.c1.id]))
        # Wrong choice selected
        self.assertFalse(self.question.is_get_score([self.c2.id]))
        # Both choices selected
        self.assertFalse(self.question.is_get_score([self.c1.id, self.c2.id]))
        # Empty selection
        self.assertFalse(self.question.is_get_score([]))

    def test_submission_creation(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.add(self.c1)
        self.assertEqual(submission.choices.count(), 1)
        self.assertIn(self.c1, submission.choices.all())


class OnlineCourseAdminTests(TestCase):
    def test_admin_classes_exist(self):
        self.assertTrue(issubclass(QuestionInline, (admin.StackedInline, admin.TabularInline)))
        self.assertTrue(issubclass(ChoiceInline, (admin.StackedInline, admin.TabularInline)))
        self.assertTrue(issubclass(QuestionAdmin, admin.ModelAdmin))
        self.assertTrue(issubclass(LessonAdmin, admin.ModelAdmin))

    def test_admin_registration(self):
        self.assertIn(Question, admin.site._registry)
        self.assertIn(Lesson, admin.site._registry)
        self.assertIn(Course, admin.site._registry)
        self.assertIn(Choice, admin.site._registry)
        self.assertIn(Submission, admin.site._registry)


class OnlineCourseViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='examtaker', password='password123')
        self.course = Course.objects.create(name='Django Final Course', description='Course Description')
        self.lesson = Lesson.objects.create(title='Core Lesson', course=self.course, content='Core content')
        self.question = Question.objects.create(
            lesson=self.lesson,
            course=self.course,
            question_text='Sample Question?',
            grade=1
        )
        self.choice_correct = Choice.objects.create(question=self.question, choice_text='Correct Choice', is_correct=True)
        self.choice_wrong = Choice.objects.create(question=self.question, choice_text='Wrong Choice', is_correct=False)
        self.client.login(username='examtaker', password='password123')

    def test_course_detail_view(self):
        response = self.client.get(reverse('onlinecourse:course_details', kwargs={'pk': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Final Course')
        self.assertContains(response, 'Sample Question?')

    def test_submit_and_exam_result(self):
        # Submit correct answer
        submit_url = reverse('onlinecourse:submit', kwargs={'course_id': self.course.id})
        post_data = {
            f'choice_{self.choice_correct.id}': str(self.choice_correct.id),
        }
        response = self.client.post(submit_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Congratulations')
        self.assertContains(response, '1/1')
        self.assertContains(response, 'Correct Choice')
