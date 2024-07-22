from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    pre_view = models.ImageField(
        upload_to="course/", verbose_name="превью ", **NULLABLE
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return f"{self.title}, {self.description}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("title",)


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="навзвание")
    description = models.TextField(verbose_name="описание")
    pre_view = models.ImageField(upload_to="lesson/", verbose_name="превью", **NULLABLE)
    video_url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return f"{self.title}, {self.description}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f"{self.user}, {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
