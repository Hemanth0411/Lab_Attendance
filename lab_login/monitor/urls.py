from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-students/', views.add_students, name='add_students'),
    path('student-list/', views.student_list, name='student_list'),
]
