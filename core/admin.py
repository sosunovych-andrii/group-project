# Register your models here.

from django.contrib import admin
from .models import (
    Forum, Comment, Grade, Event, 
    Announcement, Survey, SurveyPage, SurveyAnswer
)

# --- 1. ФОРУМИ ТА КОМЕНТАРІ ---

class CommentInline(admin.TabularInline):
    """Дозволяє бачити та редагувати коментарі прямо всередині сторінки Форуму"""
    model = Comment
    extra = 1  # Кількість порожніх рядків для нових коментарів


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'post_date', 'comments_count')
    list_filter = ('post_date', 'creator')
    search_fields = ('title', 'forum', 'creator__username')
    date_hierarchy = 'post_date'  # Зручна навігація за календарем вгорі
    inlines = [CommentInline]  # Інтегруємо коментарі у форум

    def comments_count(self, obj):
        """Рахує кількість коментарів до теми"""
        return obj.comments.count()
    comments_count.short_description = 'Кількість коментарів'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'forum', 'creator', 'post_date', 'short_text')
    list_filter = ('post_date', 'creator', 'forum')
    search_fields = ('comment', 'creator__username', 'forum__title')

    def short_text(self, obj):
        """Обрізає довгий текст коментаря в загальному списку"""
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    short_text.short_description = 'Текст коментаря'


# --- 2. ОЦІНКИ (ЖУРНАЛ) ---

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'teacher', 'date')
    list_filter = ('subject', 'grade', 'date', 'teacher')
    search_fields = ('student__username', 'teacher__username', 'subject')
    list_editable = ('grade',)  # Можна швидко виставити чи змінити оцінку зі списку
    list_per_page = 20  # Пагінація: по 20 оцінок на сторінку


# --- 3. ПОДІЇ ТА ОГОЛОШЕННЯ ---

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'start_date', 'end_date')
    list_filter = ('start_date', 'creator')
    search_fields = ('title', 'description', 'creator__username')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_date')
    list_filter = ('created_date', 'creator')
    search_fields = ('title', 'content', 'creator__username')


# --- 4. ОПИТУВАННЯ (СКЛАДНА СТРУКТУРА) ---

class SurveyAnswerInline(admin.TabularInline):
    """Показує відповіді всередині Питання"""
    model = SurveyAnswer
    extra = 3


@admin.register(SurveyPage)
class SurveyPageAdmin(admin.ModelAdmin):
    list_display = ('question', 'survey')
    list_filter = ('survey',)
    search_fields = ('question',)
    inlines = [SurveyAnswerInline]  # Відповіді редагуються прямо в питанні


class SurveyPageInline(admin.StackedInline):
    """Показує питання всередині Опитування (картками)"""
    model = SurveyPage
    extra = 1


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'completed')
    list_filter = ('completed', 'creator')
    search_fields = ('title', 'creator__username')
    list_editable = ('completed',)  # Можна закривати/відкривати опитування в 1 клік
    inlines = [SurveyPageInline]  # Питання редагуються прямо в опитуванні
