from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (
    LessonViewSet,
    CourseListAPIView,
    CourseCreateAPIView,
    CourseUpdateAPIView,
    CourseRetrieveAPIView,
    CourseDestroyAPIView,
)
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", LessonViewSet)

urlpatterns = [
    path("course/", CourseListAPIView.as_view(), name="courses"),
    path("course/<int:pk>/", CourseRetrieveAPIView.as_view(), name="courses_retrieve"),
    path("course/create/", CourseCreateAPIView.as_view(), name="course_create"),
    path(
        "course/<int:pk>/update/", CourseUpdateAPIView.as_view(), name="course_update"
    ),
    path(
        "course/<int:pk>/delete/", CourseDestroyAPIView.as_view(), name="course_delete"
    ),
] + router.urls
