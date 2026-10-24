from django import forms
from .models import Forum, Comment, Grade, Announcement, Event, Survey, SurveyAnswer, SurveyPage


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title', 'forum')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment')

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade', 'subject', 'student')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'start_date', 'end_date')


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title')


class SurveyPageForm(forms.ModelForm):
    class Meta:
        model = SurveyPage
        fields = ('question')


class SurveyAnswerForm(forms.ModelForm):
    class Meta:
        model = SurveyAnswer
        fields = ('answer')