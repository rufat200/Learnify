from rest_framework import generics, permissions
from django.db.models import Max

from ..users.permissions import IsTeacher, IsOwnerOrReadOnly
from . import models, serializers


class CourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        return models.Course.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]
    
class CourseRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeacher, IsOwnerOrReadOnly]



class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return models.Lesson.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        last_order = models.Lesson.objects.filter(course_id=course_id).aggregate(
            max_order=Max('order')
        )['max_order'] or 0
        serializer.save(course_id=course_id, order=last_order + 1)

    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

class LessonRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeacher, IsOwnerOrReadOnly]



class AssignmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.AssignmentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return models.Assignment.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_id']
        serializer.save(lesson_id=lesson_id)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

class AssignmentRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AssignmentSerializer
    queryset = models.Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeacher, IsOwnerOrReadOnly]
