from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from education.models import Test, Question, Answer, UserAnswer, Section, Lesson
from .serializers import (
    TestSerializer,
    UserAnswerSerializer,
    SectionSerializer,
    LessonSerializer,
    TestGetSerializer,
)
from education.paginators import EducationPaginator
from users.permissions import IsOwner, IsTeacher, IsModer


class SectionListApiView(generics.ListAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    pagination_class = EducationPaginator


class SectionCreateApiView(generics.CreateAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [IsOwner | IsTeacher]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()


class SectionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOwner]
    queryset = Section.objects.all()


class SectionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [IsModer | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsTeacher | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = EducationPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner | IsTeacher]


class TestCreateApiView(generics.CreateAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = [IsModer | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TestListApiView(generics.ListAPIView):
    serializer_class = TestGetSerializer
    queryset = Test.objects.all()


class TestUpdateApiView(generics.UpdateAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = [IsOwner]


class TestDestroyApiView(generics.DestroyAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = [IsOwner | IsModer]


class TestRetrieveApiView(generics.RetrieveAPIView):
    queryset = Test.objects.prefetch_related("questions__answers")
    serializer_class = TestGetSerializer


class SubmitAnswersView(APIView):

    def post(self, request, pk):
        test = Test.objects.get(pk=pk)
        serializer = UserAnswerSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        user = request.user
        answers_data = serializer.validated_data

        correct_count = 0
        total = test.questions.count()

        for ans in answers_data:
            q_num = ans["question_number"]
            a_num = ans["answer_number"]

            try:
                question = Question.objects.get(test=test, number=q_num)
            except Question.DoesNotExist:
                return Response(
                    {
                        "error": f"Вопрос с номером {q_num} не найден в тесте '{test.title}'."
                    },
                    status=400,
                )

            try:
                answer = Answer.objects.get(question=question, number=a_num)
            except Answer.DoesNotExist:
                return Response(
                    {"error": f"У вопроса {q_num} нет ответа с номером {a_num}."},
                    status=400,
                )

            UserAnswer.objects.update_or_create(
                user=user, question=question, defaults={"answer": answer}
            )

            if answer.is_correct:
                correct_count += 1

        return Response(
            {
                "test": test.title,
                "correct": correct_count,
                "total": total,
                "score": f"{round((correct_count / total) * 100, 2)} %",
            }
        )
