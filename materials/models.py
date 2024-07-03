from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    image = models.ImageField(
        upload_to="materials/images", verbose_name="Image", **NULLABLE
    )
    description = models.TextField(verbose_name="Description", **NULLABLE)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    image = models.ImageField(
        upload_to="materials/images", verbose_name="Image", **NULLABLE
    )
    link = models.URLField(verbose_name="Link", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Course", **NULLABLE
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
