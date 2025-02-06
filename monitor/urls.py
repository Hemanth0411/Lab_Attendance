from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-students/', views.add_students, name='add_students'),
    path('student-list/', views.student_list, name='student_list'),
    path('delete-student/<str:roll_no>/', views.delete_student, name='delete_student'),
    path('edit-student/<str:roll_no>/', views.edit_student, name='edit_student'),
    path('record_attendance/', views.record_attendance, name='record_attendance'),
    path('attendance_summary/', views.attendance_summary, name='attendance_summary'),
    path('attendance/success/', views.attendance_success, name='attendance_success'),
    path('session-summary/', views.session_summary, name='session_summary'),
    path('sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('import_students/', views.import_students, name='import_students'),
    path('clear-session-records/', views.clear_session_records, name='clear_session_records'),
    path('upload-sessions/', views.upload_sessions, name='upload_sessions'),
    path('reduce-attendance/', views.reduce_attendance, name='reduce_attendance'),
    path('clear_records/', views.clear_student_records, name='clear_student_records'),
    path('faqs/', views.faqs, name='faqs'),
]
