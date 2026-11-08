from optparse import Option

from django.core.exceptions import PermissionDenied
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Forum, Comment, Grade, Event, Announcement, Survey, SurveyPage, SurveyAnswer, Poll, PollOption, SurveySubmission, SurveyResponse, Vote, GalleryItem, Material, MaterialAttachment, Portfolio, PortfolioAttachment, PortfolioItem
from .forms import ForumForm, CommentForm, GradeForm, EventForm, AnnouncementForm, SurveyForm, SurveyPageForm, \
    SurveyAnswerForm, PollForm, PollOptionForm, SurveySubmissionForm, VoteForm, GalleryItemForm, MaterialForm, \
    MaterialAttachmentForm, Portfolio, PortfolioAttachmentForm, PortfolioItemForm, PortfolioForm


# Create your views here.
class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'


class ForumDetailView(DetailView):
    model = Forum
    context_object_name = 'forum'


class ForumCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Forum
    form_class = ForumForm
    context_object_name = 'forum'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ForumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Forum
    form_class = ForumForm
    context_object_name = 'forum'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff


class ForumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Forum
    context_object_name = 'forum'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(forum_id = self.kwargs['forum_pk'])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    context_object_name = 'comment'
    success_url = reverse_lazy('')

    def get_forum(self):
        return Forum.objects.get(pk = self.kwargs['forum_pk'])

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.forum = self.get_forum()
        return super().form_valid(form)


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    context_object_name = 'grades'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Grade.objects.all()

        return Grade.objects.filter(student = self.request.user)


class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    form_class = GradeForm
    context_object_name = 'grade'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    context_object_name = 'grade'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff


class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grade
    context_object_name = 'grade'
    success_url = reverse_lazy('')

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
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    context_object_name = 'event'
    success_url = reverse_lazy('')

    def test_func(self):
        event = self.get_object()

        return event.creator == self.request.user or self.request.user.is_staff


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('')

    def test_func(self):
        event = self.get_object()

        return event.creator == self.request.user or self.request.user.is_staff


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = 'announcements'


class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    context_object_name = 'announcement'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    context_object_name = 'announcement'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff


class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    context_object_name = 'announcement'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.request.user.is_staff


class SurveyListView(ListView):
    model = Survey
    context_object_name = 'surveys'


class SurveyCreateView(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    context_object_name = 'survey'
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class SurveyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    context_object_name = 'survey'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class SurveyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Survey
    context_object_name = 'survey'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class SurveyDetailView(DetailView):
    model = Survey
    context_object_name = 'survey'


class SurveyPageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SurveyPage
    form_class = SurveyPageForm
    context_object_name = 'page'
    success_url = reverse_lazy('')

    def get_survey(self):
        return Survey.objects.get(pk = self.kwargs['survey_pk'])

    def test_func(self):
        return self.get_survey().creator == self.request.user

    def form_valid(self, form):
        form.instance.survey = self.get_survey()
        return super().form_valid(form)


class SurveyPageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SurveyPage
    form_class = SurveyPageForm
    context_object_name = 'page'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().survey.creator == self.request.user


class SurveyPageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SurveyPage
    context_object_name = 'page'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().survey.creator == self.request.user


class SurveyAnswerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SurveyAnswer
    form_class = SurveyAnswerForm
    context_object_name = 'answer'
    success_url = reverse_lazy('')

    def get_page(self):
        return SurveyPage.objects.get(pk = self.kwargs['page_pk'])

    def test_func(self):
        return self.get_page().survey.creator == self.request.user

    def form_valid(self, form):
        form.instance.page = self.get_page()
        return super().form_valid(form)


class SurveyAnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SurveyAnswer
    form_class = SurveyAnswerForm
    context_object_name = 'answer'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().page.survey.creator == self.request.user


class SurveyAnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SurveyAnswer
    context_object_name = 'answer'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().page.survey.creator == self.request.user


class SurveySubmissionCreateView(LoginRequiredMixin, FormView):
    form_class = SurveySubmissionForm
    template_name = ''

    def get_survey(self):
        return get_object_or_404(Survey, pk = self.kwargs['survey_pk'])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        survey = self.get_survey()
        already_submitted = SurveySubmission.objects.filter(survey = survey, user = request.user).exists()

        if already_submitted:
            raise PermissionDenied('You have already submitted this survey')

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = self.get_survey()
        return kwargs

    def form_valid(self, form):
        survey = self.get_survey()

        try:
            with transaction.atomic():
                submission = SurveySubmission.objects.create(survey = survey, user = self.request.user)
                responses = []

                for page in form.pages:
                    answer = form.cleaned_data[f'page_{page.pk}']

                    responses.append(
                        SurveyResponse(submission = submission, page = page, answer = answer)
                    )

                SurveyResponse.objects.bulk_create(responses)
        except IntegrityError:
            form.add_error(None, 'You have already submitted this survey')
            return self.form_invalid(form)

        return  super().form_valid(form)


class SurveyResultsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Survey
    context_object_name = 'survey'
    template_name = ''

    def test_func(self):
        survey = self.get_object()
        return survey.creator == self.request.user or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.object
        context['total_submissions'] = survey.submissions.count()
        results = []

        for page in survey.pages.all():
            total_responses = page.responses.filter( submission__survey = survey).count()
            answers = []

            for answer in page.answers.all():
                count = answer.responses.filter(submission__survey = survey).count()
                percentage = 0

                if total_responses > 0:
                    percentage = count / total_responses * 100

                answers.append({
                    'answer': answer,
                    'count': count,
                    'percentage': percentage
                })

            results.append({
                'page': page,
                'total_responses': total_responses,
                'answers': answers
            })

        context['results'] = results
        return context


class PollListView(ListView):
    model = Poll
    context_object_name = 'polls'


class PollDetailView(DetailView):
    model = Poll
    context_object_name = 'poll'


class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    context_object_name = 'poll'
    form_class = PollForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PollUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Poll
    form_class = PollForm
    context_object_name = 'poll'

    def test_func(self):
        return self.get_object().creator == self.request.user or self.request.user.is_staff


class PollDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Poll
    context_object_name = 'poll'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class PollOptionListView(ListView):
    model = PollOption
    context_object_name = 'poll_options'
    success_url = reverse_lazy('')

    def get_queryset(self):
        return PollOption.objects.filter(poll_id = self.kwargs['poll_pk'])


class PollOptionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PollOption
    context_object_name = 'poll_option'
    form_class = PollOptionForm
    success_url = reverse_lazy('')

    def get_poll(self):
        return Poll.objects.get(pk = self.kwargs['poll_pk'])

    def form_valid(self, form):
        form.instance.poll = self.get_poll()
        return super().form_valid(form)

    def test_func(self):
        return self.get_poll().creator == self.request.user


class PollOptionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PollOption
    form_class = PollOptionForm
    context_object_name = 'poll_option'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().poll.creator == self.request.user


class PollOptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PollOption
    context_object_name = 'poll_option'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().poll.creator == self.request.user


class VoteCreateView(LoginRequiredMixin, FormView):
    form_class = VoteForm

    def get_poll(self):
        return get_object_or_404(Poll, pk = self.kwargs['poll_pk'])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        poll = self.get_poll()

        if poll.options.count() < 2:
            raise PermissionDenied('This poll does not have enough options.')

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['poll'] = self.get_poll()
        return kwargs

    def form_valid(self, form):
        Vote.objects.update_or_create(
            user = self.request.user,
            poll = self.get_poll(),
            defaults = {'option': form.cleaned_data['option']}
        )

        return super().form_valid(form)


class PollResultsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Poll
    context_object_name = 'poll'
    template_name = ''

    def test_func(self):
        poll = self.get_object()
        return poll.creator == self.request.user or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.object
        total_votes = poll.votes.count()
        results = []

        for option in poll.options.all():
            count = option.votes.count()
            percentage = 0

            if total_votes > 0:
                percentage = count / total_votes * 100

            results.append({
                'option': option,
                'count': count,
                'percentage': percentage
            })

        context['total_votes'] = total_votes
        context['results'] = results

        return context


class GalleryItemListView(ListView):
    model = GalleryItem
    context_object_name = 'gallery_items'

    def get_queryset(self):
        return GalleryItem.objects.filter(uploader_id = self.kwargs['user_pk'])


class GalleryItemDetailView(DetailView):
    model = GalleryItem
    context_object_name = 'gallery_item'


class GalleryItemCreateView(LoginRequiredMixin, CreateView):
    model = GalleryItem
    context_object_name = 'gallery_item'
    form_class = GalleryItemForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class GalleryItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GalleryItem
    context_object_name = 'gallery_item'
    form_class = GalleryItemForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().uploader == self.request.user


class GalleryItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GalleryItem
    context_object_name = 'gallery_item'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().uploader == self.request.user


class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    context_object_name = 'materials'

    def get_queryset(self):
        return Material.objects.filter(creator_id = self.kwargs['user_pk'])


class MaterialDetailView(DetailView):
    model = Material
    context_object_name = 'material'


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    context_object_name = 'material'
    form_class = MaterialForm
    success_url = reverse_lazy('')

    def get_material(self):
        return get_object_or_404(Material, pk = self.kwargs['material_pk'])

    def form_valid(self, form):
        form.instance.material = self.get_material()
        return super().form_valid(form)


class MaterialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Material
    context_object_name = 'material'
    form_class = MaterialForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class MaterialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Material
    context_object_name = 'material'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class MaterialAttachmentListView(LoginRequiredMixin, ListView):
    model = MaterialAttachment
    context_object_name = 'material_attachments'

    def get_queryset(self):
        return MaterialAttachment.objects.filter(material_id = self.kwargs['material_pk'])


class MaterialAttachmentDetailView(DetailView):
    model = MaterialAttachment
    context_object_name = 'material_attachment'


class MaterialAttachmentCreateView(LoginRequiredMixin, CreateView):
    model = MaterialAttachment
    context_object_name = 'material_attachment'
    form_class = MaterialAttachmentForm
    success_url = reverse_lazy('')

    def get_material(self):
        return get_object_or_404(Material, pk = self.kwargs['material_pk'], creator = self.request.user)

    def form_valid(self, form):
        form.instance.material = self.get_material()
        return super().form_valid(form)

class MaterialAttachmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MaterialAttachment
    context_object_name = 'material_attachment'
    form_class = MaterialAttachmentForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().material.creator == self.request.user


class MaterialAttachmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MaterialAttachment
    context_object_name = 'material_attachment'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().material.creator == self.request.user


class PortfolioDetailView(DetailView):
    model = Portfolio
    context_object_name = 'portfolio'


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    context_object_name = 'portfolio'
    form_class = PortfolioForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    context_object_name = 'portfolio'
    form_class = PortfolioForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class PortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Portfolio
    context_object_name = 'portfolio'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().creator == self.request.user


class PortfolioItemListView(LoginRequiredMixin, ListView):
    model = PortfolioItem
    context_object_name = 'portfolio_items'

    def get_queryset(self):
        return PortfolioItem.objects.filter(portfolio_id = self.kwargs['portfolio_pk'])


class PortfolioItemDetailView(DetailView):
    model = PortfolioItem
    context_object_name = 'portfolio_item'


class PortfolioItemCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    context_object_name = 'portfolio_item'
    form_class = PortfolioItemForm
    success_url = reverse_lazy('')

    def get_portfolio(self):
        return get_object_or_404(Portfolio, pk = self.kwargs['portfolio_pk'], creator = self.request.user)

    def form_valid(self, form):
        form.instance.portfolio = self.get_portfolio()
        return super().form_valid(form)


class PortfolioItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PortfolioItem
    context_object_name = 'portfolio_item'
    form_class = PortfolioItemForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().portfolio.creator == self.request.user


class PortfolioItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    context_object_name = 'portfolio_item'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().portfolio.creator == self.request.user


class PortfolioAttachmentListView(ListView):
    model = PortfolioAttachment
    context_object_name = 'portfolio_attachments'

    def get_queryset(self):
        return PortfolioAttachment.objects.filter(portfolio_item_id = self.kwargs['portfolio_item_pk'])


class PortfolioAttachmentDetailView(DetailView):
    model = PortfolioAttachment
    context_object_name = 'portfolio_attachment'


class PortfolioAttachmentCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioAttachment
    context_object_name = 'portfolio_attachment'
    form_class = PortfolioAttachmentForm
    success_url = reverse_lazy('')

    def get_portfolio_item(self):
        return get_object_or_404(PortfolioItem, pk = self.kwargs['portfolio_item_pk'], portfolio__creator = self.request.user)

    def form_valid(self, form):
        form.instance.portfolio_item = self.get_portfolio_item()
        return super().form_valid(form)


class PortfolioAttachmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PortfolioAttachment
    context_object_name = 'portfolio_attachment'
    form_class = PortfolioAttachmentForm
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().portfolio_item.portfolio.creator == self.request.user


class PortfolioAttachmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioAttachment
    context_object_name = 'portfolio_attachment'
    success_url = reverse_lazy('')

    def test_func(self):
        return self.get_object().portfolio_item.portfolio.creator == self.request.user