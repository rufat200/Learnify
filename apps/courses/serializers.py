from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    Course, 
    Lesson, 
    Assignment, 
    Submission,
    CourseReview
)


User = get_user_model()

class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(role='student')  # ← Фильтрация по роли
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'owner', 'average_rating', 'students']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'average_rating', 'students']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        material = serializers.FileField(required=False, allow_null=True)
        fields = ['id', 'title', 'content', 'course', 'order', 'material']
        read_only_fields = ['id', 'course']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'lesson', 'due_date']
        read_only_fields = ['id', 'lesson']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'file', 'link', 'submitted_at', 'status']
        read_only_fields = ['assignment', 'student', 'submitted_at']

class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ['id', 'course', 'student', 'rating', 'text', 'created_at']
        read_only_fields = ['student', 'created_at', 'course']
    
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value
