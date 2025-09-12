from django.contrib import admin
from education.models import Test, Section, Lesson


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("owner", "title")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("owner", "title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("owner", "title")
