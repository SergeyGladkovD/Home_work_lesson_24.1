from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(title="Test Course", description="Test Course")
        self.lesson = Lesson.objects.create(title="Test Lesson", description="Test Lesson", course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test",
            "description": "Test",
            "course": self.course.pk
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Test")
        self.assertEqual(response.data['description'], "Test")
        self.assertEqual(response.data['course'], self.course.pk)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.lesson.title)
        self.assertEqual(data['description'], self.lesson.description)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        response = self.client.patch(url, data={"title": "Updated Title", "description": "Updated Description"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['description'], "Updated Description")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="Test Course")
        self.lesson = Lesson.objects.create(title="Test Lesson", description="Test Lesson", course=self.course)
        self.url = reverse("materials:subscriptions")

    def test_subscriptions_create(self):
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(self.url, data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("message"), "подписка добавлена")
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_subscriptions_delete(self):
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("message"), "подписка удалена")
        self.assertEqual(Subscription.objects.all().count(), 0)



