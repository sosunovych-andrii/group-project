from turtledemo.chaos import line

from django import forms
from .models import Forum, Comment, Grade, Announcement, Event, Survey, SurveyAnswer, SurveyPage, Poll, PollOption, Gallery, Material, MaterialAttachment, Portfolio, PortfolioAttachment, PortfolioItem


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


class SurveySubmissionForm(forms.Form):
    def __init__(self, *args, survey, **kwargs):
        super().__init__(*args, **kwargs)

        self.survey = survey
        self.pages = list( survey.pages.prefetch_related('answers'))

        for page in self.pages:
            self.fields[f'page_{page.pk}'] = forms.ModelChoiceField(
                queryset = page.answers.all(),
                widget = forms.RadioSelect,
                label = page.question,
                empty_label = None
            )

    def clean(self):
        cleaned_data = super().clean()

        if not self.pages:
            raise forms.ValidationError('No questions in this survey.')

        return cleaned_data


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title',)


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ('option',)


class VoteForm(forms.Form):
    option = forms.ModelChoiceField(
        queryset = PollOption.objects.none(),
        widget = forms.RadioSelect,
        label = 'Choose an option',
        empty_label = None
    )

    def __init__(self, *args, poll, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = poll.options.all()


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('title', "description")


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'description')


class MaterialAttachmentForm(forms.ModelForm):
    class Meta:
        model = MaterialAttachment
        fields = ('attachment_type', 'file', 'image', 'link')

    def clean(self):
        cleaned_data = super(self).clean()
        attachment_type = cleaned_data.get('attachment_type')

        file = cleaned_data.get('file')
        image = cleaned_data.get('image')
        link = cleaned_data.get('link')

        if attachment_type == 'file' and not file:
            self.add_error('file', 'Please upload a file')
        elif attachment_type == 'image' and not image:
            self.add_error('image', 'Please upload an image')
        elif attachment_type in ('link', 'youtube') and not link:
            self.add_error('link', 'Please upload a link')

        return cleaned_data


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('title', 'description')


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ('title', 'description')


class PortfolioAttachmentForm(forms.ModelForm):
    class Meta:
        model = PortfolioAttachment
        fields = ('attachment_type', 'file', 'image', 'link')

    def clean(self):
        cleaned_data = super(self).clean()
        attachment_type = cleaned_data.get('attachment_type')

        file = cleaned_data.get('file')
        image = cleaned_data.get('image')
        link = cleaned_data.get('link')

        if attachment_type == 'file' and not file:
            self.add_error('file', 'Please upload a file')
        elif attachment_type == 'image' and not image:
            self.add_error('image', 'Please upload an image')
        elif attachment_type in ('link', 'youtube') and not link:
            self.add_error('link', 'Please upload a link')

        return cleaned_data
