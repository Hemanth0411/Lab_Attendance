from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-students/', views.add_students, name='add_students'),
    path('edit-student/<str:roll_no>/', views.edit_student, name='edit_student'),
    path('student-list/', views.student_list, name='student_list'),
    path('delete-student/<str:roll_no>/', views.delete_student, name='delete_student'),
    # Add other URL patterns here
]
