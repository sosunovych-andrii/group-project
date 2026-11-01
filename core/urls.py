from django.urls import path
from . import views

urlpatterns = [
    path('forums/', views.ForumListView.as_view(), name='forum_list'),
    path('forums/create/', views.ForumCreateView.as_view(), name='forum_create'),
    path('forums/<int:pk>/update/', views.ForumUpdateView.as_view(), name='forum_update'),
    path('forums/<int:pk>/delete/', views.ForumDeleteView.as_view(), name='forum_delete'),
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    path('comments/create/', views.CommentCreateView.as_view(), name='comment_create'),

    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/create/', views.GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/update/', views.GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),

    path('surveys/', views.SurveyListView.as_view(), name='survey_list'),
    path('surveys/create/', views.SurveyCreateView.as_view(), name='survey_create'),
    path('surveys/<int:pk>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    path('surveys/<int:pk>/update/', views.SurveyUpdateView.as_view(), name='survey_update'),
    path('surveys/<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),

    path('surveys/<int:survey_pk>/pages/create/', views.SurveyPageCreateView.as_view(), name='survey_page_create'),
    path('survey-pages/<int:pk>/update/', views.SurveyPageUpdateView.as_view(), name='survey_page_update'),
    path('survey-pages/<int:pk>/delete/', views.SurveyPageDeleteView.as_view(), name='survey_page_delete'),
    path('survey-pages/<int:answer_pk>/answers/create/', views.SurveyAnswerCreateView.as_view(), name='survey_answer_create'),
    path('survey-answers/<int:pk>/update/', views.SurveyAnswerUpdateView.as_view(), name='survey_answer_update'),
    path('survey-answers/<int:pk>/delete/', views.SurveyAnswerDeleteView.as_view(), name='survey_answer_delete'),
]
