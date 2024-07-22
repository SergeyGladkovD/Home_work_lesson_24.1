from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import Validatorlink


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        validators = [Validatorlink(field='video_url')]


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [Validatorlink(field='video_url')]


class CourseDetailSerializer(ModelSerializer):
    lesson_in_course = SerializerMethodField()
    # lesson_list = SerializerMethodField()
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField(read_only=True)

    # def get_lesson_list(self, course):
    #     return [lesson.name for lesson in Lesson.objects.filter(course=course)]
    class Meta:
        model = Course
        fields = ("title", "description", "lesson_in_course", "lesson_set", 'subscription')

    def get_is_subscription(self, course):
        return Subscription.objects.filter(
            course=course, user=self.context["request"].user
        ).exists()

    @staticmethod
    def get_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
