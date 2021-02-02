from django.contrib import admin

from .models import Poll, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
        'starts_at',
        'ends_at',
    ]

    inlines = [
        QuestionInline
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['starts_at']
        return self.readonly_fields


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = [
        'content',
        'question_type',
        'poll',
    ]
    list_display = [
        'id',
        'content',
        'question_type',
        'poll',
    ]

