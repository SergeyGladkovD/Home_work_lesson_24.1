from django.views.generic import DetailView
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (checkout_session, create_stripe_price,
                            create_stripe_product, create_stripe_session)


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ("pay_day",)


class PaymentCreateApiView(CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get("paid_course")
        lesson_id = self.request.data.get("paid_lesson")
        if course_id:
            course_product = create_stripe_product(
                Course.objects.get(pk=course_id).name
            )
            course_price = create_stripe_price(
                instance.paid_course.amount, course_product
            )
            session_id, payment_link = create_stripe_session(course_price, instance.pk)
        else:
            lesson_product = create_stripe_product(
                Lesson.objects.get(pk=lesson_id).name
            )
            lesson_price = create_stripe_price(
                instance.paid_lesson.amount, lesson_product
            )
            session_id, payment_link = create_stripe_session(lesson_price, instance.pk)

        payment_status = checkout_session(session_id)
        instance.payment_status = payment_status
        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()

    class PaymentDetailView(DetailView):
        model = Payment
