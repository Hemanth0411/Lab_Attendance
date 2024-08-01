from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-students/', views.add_students, name='add_students'),
    path('student-list/', views.student_list, name='student_list'),
    path('delete-student/<str:roll_no>/', views.delete_student, name='delete_student'),
    path('edit-student/<str:roll_no>/', views.edit_student, name='edit_student'),
    path('record_attendance/', views.record_attendance, name='record_attendance'),
    path('attendance_summary/', views.attendance_summary, name='attendance_summary'),
    path('attendance/success/', views.attendance_success, name='attendance_success'),
    path('session-summary/', views.session_summary, name='session_summary'),
]
