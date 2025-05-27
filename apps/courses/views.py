from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from django.db.models import Max
from django.utils import timezone
from django.core.files.storage import default_storage

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.material:
            material_path = instance.material.path
        else:
            material_path = None
        self.perform_destroy(instance)
        if material_path and default_storage.exists(material_path):
            default_storage.delete(material_path)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_update(self, serializer):
        lesson = self.get_object()
        old_material = lesson.material.path if lesson.material else None
        old_name = lesson.material.name if lesson.material else None

        updated_instance = serializer.save()
        new_name = updated_instance.material.name if updated_instance.material else None

        if old_name != new_name and old_material and default_storage.exists(old_material):
            default_storage.delete(old_material)

        return updated_instance



class AssignmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.AssignmentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return models.Assignment.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_id']
        assignment = serializer.save(lesson_id=lesson_id)

        # уведомляем студентов курса
        channel_layer = get_channel_layer()
        course = assignment.lesson.course
        for student in course.students.all():
            async_to_sync(channel_layer.group_send)(
                f"notifications",
                {
                    "type": "send_notification",
                    "message": f"Новое задание: {assignment.title}",
                    "event_type": "new_assignment",
                }
            )
        # async_to_sync(channel_layer.group_send)(
        #     f"notifications",
        #     {
        #         "type": "send_test_notification",
        #         "message": f"Новое задание: {assignment.title}",
        #         "event_type": "new_assignment",
        #     }
        # )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

class AssignmentRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AssignmentSerializer
    queryset = models.Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeacher, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        assignment = serializer.save()
        channel_layer = get_channel_layer()
        course = assignment.lesson.course

        for student in course.students.all():
            async_to_sync(channel_layer.group_send)(
                f"user_{student.id}",
                {
                    "type": "send_notification",
                    "message": f"Задание обновлено: {assignment.title}",
                    "event_type": "updated_assignment",
                }
            )

    def perform_destroy(self, instance):
        title = instance.title
        course = instance.lesson.course
        instance.delete()

        channel_layer = get_channel_layer()
        for student in course.students.all():
            async_to_sync(channel_layer.group_send)(
                f"user_{student.id}",
                {
                    "type": "send_notification",
                    "message": f"Задание удалено: {title}",
                    "event_type": "deleted_assignment",
                }
            )



class SubmissionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return models.Submission.objects.filter(assignment_id=assignment_id)

    def perform_create(self, serializer):
        user = self.request.user
        assignment_id = self.kwargs['assignment_id']
        assignment = models.Assignment.objects.get(id=assignment_id)

        if user.role != 'student':
            raise ValidationError("Только студенты могут отправлять задания")
        
        if models.Submission.objects.filter(assignment=assignment, student=user).exists():
            raise ValidationError('Вы уже отправили это задание')
        
        now = timezone.now()
        io_time = now <= assignment.due_date if assignment.due_date else True
        
        serializer.save(student=user, assignment=assignment, status=io_time)

class SubmissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        submission = self.get_object()
        old_file = submission.file.path if submission.file else None
        old_name = submission.file.name if submission.file else None

        updated_instance = serializer.save()
        new_name = updated_instance.file.name if updated_instance.file else None

        if old_name != new_name and old_file and default_storage.exists(old_file):
            default_storage.delete(old_file)

        return updated_instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file:
            file_path = instance.file.path
        else:
            file_path = None
        self.perform_destroy(instance)
        if file_path and default_storage.exists(file_path):
            default_storage.delete(file_path)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CourseReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return models.CourseReview.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']

        course = models.Course.objects.get(id=course_id)
        if self.request.user.role != 'student':
            raise ValidationError("Только студенты могут оставлять отзывы")

        if models.CourseReview.objects.filter(course=course, student=self.request.user).exists():
            raise ValidationError("Вы уже оставили отзыв на этот курс")

        review = serializer.save(course=course, student=self.request.user)

        channel_layer = get_channel_layer()
        teacher = course.owner

        async_to_sync(channel_layer.group_send)(
            f"user_{teacher.id}",
            {
                "type": "send_notification",
                "message": f"Новый отзыв от {self.request.user.email} на курс '{course.title}'",
                "event_type": "new_review",
            }
        )
