from django.urls import path

from .apps import EducationConfig
from .views import (
    SubmitAnswersView,
    SectionCreateApiView,
    SectionListApiView,
    SectionRetrieveAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    TestCreateApiView,
    TestUpdateApiView,
    TestListApiView,
    TestDestroyApiView,
    TestRetrieveApiView,
)

app_name = EducationConfig.name

urlpatterns = [
    path("section/create/", SectionCreateApiView.as_view(), name="section_create"),
    path("sections/", SectionListApiView.as_view(), name="section_list"),
    path("section/<int:pk>/", SectionRetrieveAPIView.as_view(), name="section_get"),
    path(
        "section/update/<int:pk>/",
        SectionUpdateAPIView.as_view(),
        name="section_update",
    ),
    path(
        "section/delete/<int:pk>/",
        SectionDestroyAPIView.as_view(),
        name="lesson_delete",
    ),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("test/create/", TestCreateApiView.as_view(), name="test_create"),
    path("tests/", TestListApiView.as_view(), name="test_list"),
    path("test/<int:pk>/", TestRetrieveApiView.as_view(), name="test_get"),
    path("test/update/<int:pk>/", TestUpdateApiView.as_view(), name="test_update"),
    path("test/delete/<int:pk>/", TestDestroyApiView.as_view(), name="test_delete"),
    path("test/<int:pk>/submit/", SubmitAnswersView.as_view(), name="submit_answer"),
]
