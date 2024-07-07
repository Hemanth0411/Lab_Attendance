from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email_id"]

@admin.register(Departments)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["department_name"]