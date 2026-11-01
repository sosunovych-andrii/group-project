from django import forms
from .models import Forum, Comment, Grade, Announcement, Event, Survey, SurveyAnswer, SurveyPage, Poll, PollOption


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title', 'forum')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

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

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError('End date cannot be before start date')

        return cleaned_data


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title',)


class SurveyPageForm(forms.ModelForm):
    class Meta:
        model = SurveyPage
        fields = ('question', 'order')


class SurveyAnswerForm(forms.ModelForm):
    class Meta:
        model = SurveyAnswer
        fields = ('answer',)
