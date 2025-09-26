from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Section, Lesson, Test, UserAnswer, Question, Answer
from users.models import User


class SectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@lms.ru")
        self.client.force_authenticate(self.user)
        self.section = Section.objects.create(
            title="Test Section", description="Test Description", owner=self.user
        )

    def test_create_section(self):
        """Тестирование создания раздела"""
        self.data = {"title": "Test", "description": "Test"}

        response = self.client.post("/section/create/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "description": "Test",
                "title": "Test",
                "number_of_lessons": 0,
                "lessons": [],
                "owner": 1,
            },
        )

        self.assertTrue(Section.objects.all().exists())

    def test_list_section(self):
        """Тестирование списка разделов"""
        section = Section.objects.create(
            title="Test", description="Test", owner=self.user
        )

        response = self.client.get("/sections/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.json()["results"][0]

        self.assertEqual(
            result,
            {
                "id": section.id,
                "description": "Test",
                "title": "Test",
                "number_of_lessons": 0,
                "lessons": [],
                "owner": self.user.id,
            },
        )

    def test_update_section(self):
        """Тестированрие для обновления раздела"""
        section = Section.objects.create(
            title="Test", description="Test", owner=self.user
        )

        self.data = {
            "title": "Test 1",
            "description": "Test 1",
            "number_of_lessons": 0,
            "lessons": [],
        }

        response = self.client.put(f"/section/update/{section.id}/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": section.id,
                "description": "Test 1",
                "title": "Test 1",
                "number_of_lessons": 0,
                "lessons": [],
                "owner": self.user.id,
            },
        )

    def test_delete_section(self):
        """Тестирование удаления раздела"""
        section = Section.objects.create(
            title="Test", description="Test", owner=self.user
        )
        response = self.client.delete(
            f"/section/delete/{section.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@lms.ru")
        self.client.force_authenticate(self.user)
        self.section = Section.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""
        self.data = {"title": "Test", "description": "Test", "section": self.section.id}

        response = self.client.post("/lesson/create/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["title"], "Test")
        self.assertEqual(response_data["description"], "Test")
        self.assertEqual(response_data["section"], self.section.id)
        self.assertEqual(response_data["owner"], self.user.id)

        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lessons(self):
        """Тестирование списка уроков"""
        lesson = Lesson.objects.create(
            title="Test", description="Test", section=self.section, owner=self.user
        )

        response = self.client.get("/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json().get("results", [])

        result = results[0]

        self.assertEqual(result["id"], lesson.id)
        self.assertEqual(result["title"], "Test")
        self.assertEqual(result["description"], "Test")
        self.assertEqual(result["section"], self.section.id)
        self.assertEqual(result["owner"], self.user.id)

    def test_update_lesson(self):
        """Тестированрие для обновления урока"""
        lesson = Lesson.objects.create(
            title="Test", description="Test", section=self.section, owner=self.user
        )

        self.data = {
            "title": "Test 1",
            "description": "Test 1",
            "section": self.section.id,
        }

        response = self.client.put(f"/lesson/update/{lesson.id}/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["title"], "Test 1")
        self.assertEqual(response_data["description"], "Test 1")
        self.assertEqual(response_data["section"], self.section.id)
        self.assertEqual(response_data["owner"], self.user.id)

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        lesson = Lesson.objects.create(
            title="Test", description="Test", section=self.section, owner=self.user
        )
        response = self.client.delete(
            f"/lesson/delete/{lesson.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@lms.ru")
        self.client.force_authenticate(self.user)
        self.section = Section.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Course",
            description="Test Description",
            section=self.section,
            owner=self.user,
        )

    def test_create_test(self):
        """Тестирование создания теста"""
        self.data = {
            "title": "Тест по истории Древнего Рима",
            "description": "Проверка знаний по истории Древнего Рима",
            "lesson": self.lesson.id,
            "questions": [
                {
                    "number": 1,
                    "question": "В каком году был основан Рим?",
                    "answers": [
                        {"number": 1, "answer": "753 год до н.э.", "is_correct": True},
                        {"number": 2, "answer": "509 год до н.э.", "is_correct": False},
                    ],
                }
            ],
        }

        response = self.client.post("/test/create/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["title"], "Тест по истории Древнего Рима")
        self.assertEqual(
            response_data["description"], "Проверка знаний по истории Древнего Рима"
        )
        self.assertEqual(response_data["lesson"], self.lesson.id)
        self.assertEqual(response_data["owner"], self.user.id)
        self.assertEqual(len(response_data["questions"]), 0)

        self.assertTrue(Lesson.objects.all().exists())

    def test_list_test(self):
        """ Тестирование получение списка тестов """
        create_data = {
            "title": "Тест по истории Древнего Рима",
            "description": "Проверка знаний по истории Древнего Рима",
            "lesson": self.lesson.id,
            "questions": [
                {
                    "number": 1,
                    "question": "В каком году был основан Рим?",
                    "answers": [
                        {"number": 1, "answer": "753 год до н.э.", "is_correct": True},
                        {"number": 2, "answer": "509 год до н.э.", "is_correct": False},
                    ],
                }
            ],
        }

        create_response = self.client.post(
            "/test/create/", data=create_data, format="json"
        )
        test_id = create_response.json()["id"]

        response = self.client.get("/tests/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertTrue(len(response_data) > 0)

        result = response_data[0]
        self.assertEqual(result["id"], test_id)
        self.assertEqual(result["title"], "Тест по истории Древнего Рима")

    def test_update_test(self):
        """Тестированрие для обновления теста"""
        create_data = {
            "title": "Test",
            "description": "Test",
            "lesson": self.lesson.id,
            "questions": [
                {
                    "number": 1,
                    "question": "В каком году был основан Рим?",
                    "answers": [
                        {"number": 1, "answer": "753 год до н.э.", "is_correct": True},
                        {"number": 2, "answer": "509 год до н.э.", "is_correct": False},
                    ],
                }
            ],
        }

        create_response = self.client.post(
            "/test/create/", data=create_data, format="json"
        )
        test_id = create_response.json()["id"]

        update_data = {
            "title": "Test 1",
            "description": "Test 1",
            "lesson": self.lesson.id,
        }

        response = self.client.put(
            f"/test/update/{test_id}/", data=update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["title"], "Test 1")
        self.assertEqual(response_data["description"], "Test 1")

    def test_delete_test(self):
        """Тестирование удаления теста"""
        create_data = {
            "title": "Test",
            "description": "Test",
            "lesson": self.lesson.id,
            "questions": [
                {
                    "number": 1,
                    "question": "В каком году был основан Рим?",
                    "answers": [
                        {"number": 1, "answer": "753 год до н.э.", "is_correct": True},
                        {"number": 2, "answer": "509 год до н.э.", "is_correct": False},
                    ],
                }
            ],
        }

        create_response = self.client.post(
            "/test/create/", data=create_data, format="json"
        )
        test_id = create_response.json()["id"]

        response = self.client.delete(f"/test/delete/{test_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserAnswerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@lms.ru")
        self.client.force_authenticate(user=self.user)

        self.test = Test.objects.create(
            title="Тест по математике",
            description="Проверка знаний по математике",
            owner=self.user,
        )

        self.question1 = Question.objects.create(
            test=self.test, number=1, question="Сколько будет 2 + 2?"
        )

        self.question2 = Question.objects.create(
            test=self.test, number=2, question="Сколько будет 3 * 3?"
        )

        self.answer1_correct = Answer.objects.create(
            question=self.question1, number=1, answer="4", is_correct=True
        )

        self.answer1_wrong = Answer.objects.create(
            question=self.question1, number=2, answer="5", is_correct=False
        )

        self.answer2_correct = Answer.objects.create(
            question=self.question2, number=1, answer="9", is_correct=True
        )

        self.answer2_wrong = Answer.objects.create(
            question=self.question2, number=2, answer="6", is_correct=False
        )

    def test_user_answer_creation(self):
        """Тестирование создания ответа пользователя"""
        user_answer = UserAnswer.objects.create(
            user=self.user, question=self.question1, answer=self.answer1_correct
        )

        self.assertEqual(user_answer.user, self.user)
        self.assertEqual(user_answer.question, self.question1)
        self.assertEqual(user_answer.answer, self.answer1_correct)
        self.assertIsNotNone(user_answer.submitted_at)

    def test_submit_answers_success(self):
        """Тестирование успешной отправки ответов"""
        data = [
            {"question_number": 1, "answer_number": 1},
            {"question_number": 2, "answer_number": 1},
        ]

        response = self.client.post(
            f"/test/{self.test.id}/submit/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["test"], "Тест по математике")
        self.assertEqual(response_data["correct"], 2)
        self.assertEqual(response_data["total"], 2)
        self.assertEqual(response_data["score"], "100.0 %")

        data2 = [
            {"question_number": 1, "answer_number": 2},
            {"question_number": 2, "answer_number": 1},
        ]

        response2 = self.client.post(
            f"/test/{self.test.id}/submit/", data=data2, format="json"
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json()["correct"], 1)

        updated_answer = UserAnswer.objects.get(user=self.user, question=self.question1)
        self.assertEqual(updated_answer.answer, self.answer1_wrong)

    def test_submit_answers_partial_correct(self):
        """Тестирование частично правильных ответов"""
        data = [
            {"question_number": 1, "answer_number": 1},
            {"question_number": 2, "answer_number": 2},
        ]

        response = self.client.post(
            f"/test/{self.test.id}/submit/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["correct"], 1)
        self.assertEqual(response_data["total"], 2)
        self.assertEqual(response_data["score"], "50.0 %")

    def test_submit_answers_none_correct(self):
        """Тестирование полностью неправильных ответов"""
        data = [
            {"question_number": 1, "answer_number": 2},
            {"question_number": 2, "answer_number": 2},
        ]

        response = self.client.post(
            f"/test/{self.test.id}/submit/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["correct"], 0)
        self.assertEqual(response_data["total"], 2)
        self.assertEqual(response_data["score"], "0.0 %")

    def test_submit_answers_unauthorized(self):
        """Тестирование доступа без авторизации"""
        self.client.logout()

        data = [{"question_number": 1, "answer_number": 1}]

        response = self.client.post(
            f"/test/{self.test.id}/submit/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
