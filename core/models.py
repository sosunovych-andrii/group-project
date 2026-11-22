from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length = 100)
    forum = models.TextField()
    post_date = models.DateTimeField(auto_now_add = True)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = "forums"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    post_date = models.DateTimeField(auto_now_add = True)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = "comments"
    )

    forum = models.ForeignKey(
        Forum, on_delete = models.CASCADE, related_name = 'comments'
    )

    def __str__(self):
        return self.comment

class Grade(models.Model):
    grade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )

    subject = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add = True)

    student = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'recieved_grades'
    )

    teacher = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'created_grades'
    )

    def __str__(self):
        return f'{self.student} - {self.subject}, {self.grade}'


class Event(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'events'
    )

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'anouncements'
    )

    def __str__(self):
        return self.title


class Survey(models.Model):
    title = models.CharField(max_length = 100)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = "surveys"
    )

    def __str__(self):
        return self.title


class SurveyPage(models.Model):
    question = models.CharField(max_length = 100)
    order = models.PositiveIntegerField(default = 0)

    survey = models.ForeignKey(
        Survey, on_delete = models.CASCADE, related_name = 'pages'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class SurveyAnswer(models.Model):
    answer = models.CharField(max_length = 100)

    page = models.ForeignKey(
        SurveyPage, on_delete = models.CASCADE, related_name = 'answers'
    )

    def __str__(self):
        return self.answer


class SurveySubmission(models.Model):
    submitted_date = models.DateTimeField(auto_now_add = True)

    survey = models.ForeignKey(
        Survey, on_delete = models.CASCADE, related_name = 'submissions'
    )

    user = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'survey_submissions'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['survey', 'user'],
                name = 'unique_survey_submission'
            )
        ]


class SurveyResponse(models.Model):
    submission = models.ForeignKey(
        SurveySubmission, on_delete = models.CASCADE, related_name = 'responses'
    )

    page = models.ForeignKey(
        SurveyPage, on_delete = models.CASCADE, related_name = 'responses'
    )

    answer = models.ForeignKey(
        SurveyAnswer, on_delete = models.CASCADE, related_name = 'responses'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['submission', 'page'],
                name = 'unique_submission_page'
            )
        ]


class Poll(models.Model):
    title = models.CharField(max_length = 100)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = "polls"
    )

    def __str__(self):
        return self.title


class PollOption(models.Model):
    option = models.CharField(max_length = 100)

    poll = models.ForeignKey(
        Poll, on_delete = models.CASCADE, related_name = 'options'
    )

    def __str__(self):
        return self.option


class Vote(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'votes'
    )

    poll = models.ForeignKey(
        Poll, on_delete = models.CASCADE, related_name = 'votes'
    )

    option = models.ForeignKey(
        PollOption, on_delete = models.CASCADE, related_name = 'votes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'poll'],
                name = 'unique_user_poll_vote'
            )
        ]


class GalleryItem(models.Model):
    title = models.CharField(max_length = 100, blank = True)
    image = models.ImageField(upload_to = 'gallery/')
    uploaded_at = models.DateTimeField(auto_now_add = True)

    uploader = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'gallery_images'
    )

    def __str__(self):
        return self.title


class Material(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    creator = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'materials'
    )

    def __str__(self):
        return self.title


class MaterialAttachment(models.Model):
    class AttachmentChoices(models.TextChoices):
        FILE = 'file', 'File'
        IMAGE = 'image', 'Image'
        LINK = 'link', 'Link'
        YOUTUBE = 'youtube', 'YouTube'

    attachment_type = models.CharField(max_length = 10, choices = AttachmentChoices.choices)
    file = models.FileField(upload_to = 'materials/files/', blank = True, null = True)
    image = models.ImageField(upload_to = 'materials/images/', blank = True, null = True)
    link = models.URLField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    material = models.ForeignKey(
        Material, on_delete = models.CASCADE, related_name = 'attachments'
    )

    def __str__(self):
        return f'{self.material} - {self.attachment_type}'


class Portfolio(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    creator = models.OneToOneField(
        User, on_delete = models.CASCADE, related_name = 'portfolio'
    )

    def __str__(self):
        return self.title


class PortfolioItem(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    portfolio = models.ForeignKey(
        Portfolio, on_delete = models.CASCADE, related_name = 'items'
    )

    def __str__(self):
        return self.title


class PortfolioAttachment(models.Model):
    class AttachmentChoices(models.TextChoices):
        FILE = 'file', 'File'
        IMAGE = 'image', 'Image'
        LINK = 'link', 'Link'

    attachment_type = models.CharField(max_length = 10, choices = AttachmentChoices.choices)
    file = models.FileField(upload_to = 'portfolio/files/', blank = True, null = True)
    image = models.ImageField(upload_to = 'portfolio/images/', blank = True, null = True)
    link = models.URLField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    portfolio_item = models.ForeignKey(
        PortfolioItem, on_delete = models.CASCADE, related_name = 'attachments'
    )

    def __str__(self):
        return f'{self.portfolio_item} - {self.attachment_type}'