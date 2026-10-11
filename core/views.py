from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Forum, Comment, Grade
from .forms import ForumForm, CommentForm, GradeForm


# Create your views here.
class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'


class ForumCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Forum
    form_class = ForumForm
    context_object_name = 'forum'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ForumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Forum
    form_class = ForumForm
    context_object_name = 'forum'

    def test_func(self):
        return self.request.user.is_staff

class ForumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Forum
    context_object_name = 'forum'

    def test_func(self):
        return self.request.user.is_staff

class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    context_object_name = 'comment'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class GradeListView(ListView):
    model = Grade
    context_object_name = 'grades'


class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    form_class = GradeForm
    context_object_name = 'grade'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.teacher = self.request.user


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    context_object_name = 'grade'

    def test_func(self):
        return self.request.user.is_staff

class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grade
    context_object_name = 'grade'

    def test_func(self):
        return self.request.user.is_staff