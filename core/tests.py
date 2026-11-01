# Create your tests here.

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import (
    Forum, Comment, Grade, Event, 
    Announcement, Survey, SurveyPage, SurveyAnswer
)
from .views import (
    ForumListView, ForumCreateView, 
    GradeCreateView, SurveyUpdateView
)
from .forms import (
    ForumForm, CommentForm, GradeForm, AnnouncementForm,
    EventForm, SurveyForm, SurveyPageForm, SurveyAnswerForm
)

class ModelsComprehensiveTestCase(TestCase):

    def setUp(self):
        self.user_teacher = User.objects.create_user(username='teacher_1', password='testpassword')
        self.user_student = User.objects.create_user(username='student_1', password='testpassword')

    def test_forum_and_comment_creation(self):
        forum_topic = Forum.objects.create(
            title="Програмування на Python",
            forum="Обговорюємо основи Django.",
            creator=self.user_teacher
        )
        self.assertEqual(forum_topic.title, "Програмування на Python")
        self.assertEqual(str(forum_topic), "Програмування на Python")
        self.assertIsNotNone(forum_topic.post_date)
        comment_text = "Дякую за тему, дуже корисно!"
        comment = Comment.objects.create(
            comment=comment_text,
            creator=self.user_student,
            forum=forum_topic
        )
        self.assertEqual(comment.comment, comment_text)
        self.assertEqual(str(comment), comment_text)   
        self.assertEqual(forum_topic.comments.count(), 1)
        self.assertEqual(forum_topic.comments.first(), comment)

    def test_grade_creation(self):
        grade_record = Grade.objects.create(
            grade=11,
            subject="Математика",
            student=self.user_student,
            teacher=self.user_teacher
        )
        self.assertEqual(grade_record.grade, 11)
        self.assertEqual(grade_record.subject, "Математика")
        
        expected_str = f'{self.user_student} - Математика, 11'
        self.assertEqual(str(grade_record), expected_str)

    def test_event_creation(self):
        start = timezone.now()
        end = start + timezone.timedelta(hours=2)
        
        event = Event.objects.create(
            title="Екзамен з Алгебри",
            description="Приготуйте калькулятори",
            start_date=start,
            end_date=end,
            creator=self.user_teacher
        )
        self.assertEqual(event.title, "Екзамен з Алгебри")
        self.assertEqual(str(event), "Екзамен з Алгебри")
        self.assertTrue(event.end_date > event.start_date)

    def test_announcement_creation(self):
        announcement = Announcement.objects.create(
            title="Канікули!",
            content="З наступного понеділка починаються осінні канікули.",
            creator=self.user_teacher
        )
        self.assertEqual(announcement.title, "Канікули!")
        self.assertEqual(str(announcement), "Канікули!")

    def test_survey_full_structure(self):
        survey = Survey.objects.create(
            title="Опитування про якість навчання",
            creator=self.user_teacher
        )
        self.assertEqual(survey.title, "Опитування про якість навчання")
        self.assertEqual(str(survey), "Опитування про якість навчання")
        self.assertFalse(survey.completed)

        question_text = "Чи подобається вам формат лекцій?"
        page = SurveyPage.objects.create(
            question=question_text,
            survey=survey
        )
        self.assertEqual(page.question, question_text)
        self.assertEqual(str(page), question_text)
        self.assertEqual(survey.surveys.count(), 1)

        answer_text = "Так, дуже зручно"
        answer = SurveyAnswer.objects.create(
            answer=answer_text,
            page=page
        )
        self.assertEqual(answer.answer, answer_text)
        self.assertEqual(str(answer), answer_text)
        self.assertEqual(page.answers.count(), 1)

class EducationalViewsRequestFactoryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        
        self.student = User.objects.create_user(username='student_user', password='password123')
        self.teacher = User.objects.create_user(username='teacher_user', password='password123', is_staff=True)
        
        self.forum = Forum.objects.create(
            title="Стара тема",
            forum="Текст теми",
            creator=self.teacher
        )
        self.survey = Survey.objects.create(
            title="Старе опитування",
            creator=self.teacher
        )


    def test_forum_list_view_accessible_by_anyone(self):
        request = self.factory.get('/core/forums/')
        view = ForumListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_forum_create_view_denied_for_student(self):
        request = self.factory.get('/core/forums/create/')
        request.user = self.student
        
        view = ForumCreateView.as_view()
        
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_forum_create_view_allowed_for_staff_and_saves_data(self):
        form_data = {
            'title': 'Новий форум від фабрики',
            'forum': 'Опис нового форуму'
        }
        request = self.factory.post('/core/forums/create/', data=form_data)
        request.user = self.teacher
        
        view = ForumCreateView.as_view(success_url='/core/forums/')
        response = view(request)
        
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(Forum.objects.filter(title='Новий форум від фабрики').exists())
        created_forum = Forum.objects.get(title='Новий форум від фабрики')
        self.assertEqual(created_forum.creator, self.teacher)


    def test_grade_create_view_saves_teacher_automatically(self):
        form_data = {
            'grade': 12,
            'subject': 'Інформатика',
            'student': self.student.id
        }
        request = self.factory.post('/core/grades/create/', data=form_data)
        request.user = self.teacher
        
        view = GradeCreateView.as_view(success_url='/core/grades/')
        response = view(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Grade.objects.filter(subject='Інформатика', grade=12).exists())
        
        grade_record = Grade.objects.get(subject='Інформатика')
        self.assertEqual(grade_record.teacher, self.teacher)



    def test_survey_update_denied_for_non_creator(self):
        request = self.factory.get(f'/core/surveys/{self.survey.pk}/update/')
        request.user = self.student
        
        view = SurveyUpdateView.as_view()
        
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.survey.pk)

    def test_survey_update_allowed_for_creator(self):
        request = self.factory.get(f'/core/surveys/{self.survey.pk}/update/')
        request.user = self.teacher
        
        view = SurveyUpdateView.as_view()
        response = view(request, pk=self.survey.pk)
        
        self.assertEqual(response.status_code, 200)

class EducationalPlatformFormsTestCase(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(username='student_for_forms', password='password123')
        self.teacher = User.objects.create_user(username='teacher_for_forms', password='password123')
        self.survey = Survey.objects.create(title="Тестове опитування", creator=self.teacher)
        self.page = SurveyPage.objects.create(question="Якесь питання?", survey=self.survey)

    def test_forum_form(self):
        form_data = {'title': 'Тема', 'forum': 'Зміст теми'}
        form = ForumForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_invalid = ForumForm(data={'title': '', 'forum': 'Текст'})
        self.assertFalse(form_invalid.is_valid())
        self.assertIn('title', form_invalid.errors)

    def test_comment_form(self):
        form_data = {'comment': 'Мій коментар'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_invalid = CommentForm(data={'comment': ''})
        self.assertFalse(form_invalid.is_valid())

    def test_grade_form(self):
        form_data = {
            'grade': 12,
            'subject': 'Математика',
            'student': self.student.id
        }
        form = GradeForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_invalid = GradeForm(data={'grade': 'дванадцять', 'subject': 'Математика', 'student': self.student.id})
        self.assertFalse(form_invalid.is_valid())
        self.assertIn('grade', form_invalid.errors)

    def test_announcement_form(self):
        form_data = {'title': 'Важливо', 'content': 'Текст оголошення'}
        form = AnnouncementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form(self):
        now = timezone.now()
        form_data = {
            'title': 'Зустріч',
            'description': 'Опис події',
            'start_date': now,
            'end_date': now + timezone.timedelta(hours=1)
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_survey_form(self):
        form_data = {'title': 'Опитування про їдальню'}
        form = SurveyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_survey_page_form(self):
        form_data = {'question': 'Вам подобається меню?'}
        form = SurveyPageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_survey_answer_form(self):
        form_data = {'answer': 'Так, дуже'}
        form = SurveyAnswerForm(data=form_data)
        self.assertTrue(form.is_valid())