from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField(default=0, help_text="Порядковый номер урока в курсе")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} (Курс: {self.course.title})'
    
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} (Урок: {self.lesson.title})'
    