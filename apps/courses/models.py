from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses') # New

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0
    
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField(default=0, help_text="Порядковый номер урока в курсе")
    material = models.FileField(upload_to='materials/', null=True)

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
    
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to='student_submissions/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True) # True - вовремя, False - опоздал

    def __str__(self):
        return f'{self.student.email} - {self.assignment.title}'
    
class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    rating = models.PositiveSmallIntegerField()  # от 1 до 5
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')  # Один отзыв от студента на курс
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.email} – {self.course.title} ({self.rating})'
