from django.urls import path

from . import views


urlpatterns = [
    path('courses/', views.CourseListCreateAPIView.as_view()),                                 # good
    path('courses/<int:pk>/', views.CourseRetrieveUpdateDeleteAPIView.as_view()),              # good
    path('courses/<int:course_id>/lessons/', views.LessonListCreateAPIView.as_view()),         # good
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDeleteAPIView.as_view()),              # good
    path('lessons/<int:lesson_id>/assignments/', views.AssignmentListCreateAPIView.as_view()), # good
    path('assignments/<int:pk>/', views.AssignmentRetrieveUpdateDeleteAPIView.as_view()),      # good
]
