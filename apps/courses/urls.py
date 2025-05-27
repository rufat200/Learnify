from django.urls import path

from . import views


urlpatterns = [
    path('courses/', views.CourseListCreateAPIView.as_view()),
    path('courses/<int:pk>/', views.CourseRetrieveUpdateDeleteAPIView.as_view()),
    path('courses/<int:course_id>/lessons/', views.LessonListCreateAPIView.as_view()),
    path('courses/<int:course_id>/reviews/', views.CourseReviewListCreateAPIView.as_view()),
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDeleteAPIView.as_view()),
    path('lessons/<int:lesson_id>/assignments/', views.AssignmentListCreateAPIView.as_view()),
    path('assignments/<int:pk>/', views.AssignmentRetrieveUpdateDeleteAPIView.as_view()),
    path('assignments/<int:assignment_id>/submit/', views.SubmissionListCreateAPIView.as_view()),
    path('submit/<int:pk>/', views.SubmissionRetrieveUpdateDestroyAPIView.as_view()),
]
