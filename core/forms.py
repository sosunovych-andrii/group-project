from django import forms
from .models import Forum, Comment, Grade


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