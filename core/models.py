from django.contrib.auth.models import User
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
    grade = models.PositiveIntegerField()
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