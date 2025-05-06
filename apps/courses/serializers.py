from rest_framework import serializers

from .models import Course, Lesson, Assignment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'order']
        read_only_fields = ['id', 'course']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'lesson', 'due_date']
        read_only_fields = ['id', 'lesson']