from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Forum, Comment
from .forms import ForumForm, CommentForm

# Create your views here.
class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'


class ForumCreateView(CreateView):
    model = Forum
    form_class = ForumForm
    context_object_name = 'forum'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ForumUpdateView(UpdateView):
    model = Forum
    form_class = ForumForm


class ForumDeleteView(DeleteView):
    model = Forum


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