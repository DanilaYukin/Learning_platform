from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from education.models import Section, Lesson, Test, Question, Answer


class AnswerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["number", "answer"]


class QuestionGetSerializer(serializers.ModelSerializer):
    answers = AnswerGetSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["number", "question", "answers"]


class TestGetSerializer(serializers.ModelSerializer):
    questions = QuestionGetSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ["id", "title", "description", "lesson", "questions", "owner"]


class LessonSerializer(ModelSerializer):
    tests = TestGetSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class SectionSerializer(ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_number_of_lessons(instance):
        return instance.lessons.count()

    class Meta:
        model = Section
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["number", "answer", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["number", "question", "answers"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ["id", "title", "description", "lesson", "questions", "owner"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        test = Test.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Question.objects.create(test=test, **question_data)

            for answer_data in answers_data:
                answer_number = answer_data.get("number")
                answer_text = answer_data.get("answer")
                is_correct = answer_data.get("is_correct", False)

                Answer.objects.create(
                    question=question,
                    number=answer_number,
                    answer=answer_text,
                    is_correct=is_correct,
                )

        return test


class UserAnswerSerializer(serializers.Serializer):
    question_number = serializers.IntegerField()
    answer_number = serializers.IntegerField()
