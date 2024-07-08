from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lesson_in_course = SerializerMethodField()
    # lesson_list = SerializerMethodField()
    lesson_set = LessonSerializer(many=True)

    # def get_lesson_list(self, course):
    #     return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "lesson_in_course", "lesson_set")
