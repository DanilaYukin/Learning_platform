from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import User


class Section(models.Model):
    """ Модель раздела """
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="владелец",
    )

    def __str__(self):
        return f"{self.id} ({self.title})"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["title"]


class Lesson(models.Model):
    """ Модель Урока """
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    material = models.FileField(
        upload_to="documents/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "doc", "docx", "txt", "xls", "xlsx"]
            )
        ],
        null=True,
        blank=True,
        verbose_name="Материал к уроку",
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="lessons", verbose_name="Раздел"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="владелец",
    )

    def __str__(self):
        return f"{self.title} ({self.section.title})"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title", "section"]


class Test(models.Model):
    """ Модель теста """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Урок"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="владелец",
    )

    def __str__(self):
        return f"{self.id} ({self.title})"


class Question(models.Model):
    """ Модель вопроса """
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    number = models.PositiveIntegerField(verbose_name="Номер вопроса")

    class Meta:
        unique_together = ("test", "number")
        ordering = ["number"]

    def __str__(self):
        return f"Вопрос {self.number}: {self.question}"


class Answer(models.Model):
    """ Модель ответа """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    number = models.PositiveIntegerField(verbose_name="Номер ответа")

    class Meta:
        unique_together = ("question", "number")
        ordering = ["number"]

    def __str__(self):
        return f"Ответ {self.number} к вопросу {self.question.number}: {self.answer}"


class UserAnswer(models.Model):
    """ Модель ответа от пользователя """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
