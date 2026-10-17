from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Forum, Comment, Grade, Event, Announcement
from .forms import ForumForm, CommentForm, GradeForm, EventForm, AnnouncementForm


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
        return super().form_valid(form)


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


class EventListView(ListView):
    model = Event
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    context_object_name = 'event'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    context_object_name = 'event'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = 'event'


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = 'announcements'


class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    context_object_name = 'announcement'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    context_object_name = 'announcement'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)